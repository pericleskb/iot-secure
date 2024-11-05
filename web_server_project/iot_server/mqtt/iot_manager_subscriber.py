import paho.mqtt.client as mqtt

from files import file_util
from ciphers_publisher import send_cipher

"""
    This class implements an MQTT subscriber and will handle all the
    incoming messages from the MQTT broker. 
    It subscribes to 2 topics.
    1. device_connected topic. Each device connected to the network will publish
       a message on this topic and wait to receive the active cipher on the
       set_cipher_suite topic.
    2. measurements topic. Receive the measurements from devices
"""
class IotManagerSubscriber:

    def __init__(self):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def start_subscribe_loop(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe

        port = 1883

        if file_util.should_use_ssl():
            # Certificates defined. Use ssl
            certs = file_util.read_certificate_conf_file()

            password = certs.get("password") if certs.get("password") else None

            self.mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                          certfile=certs.get("certfile"),
                          keyfile=certs.get("keyfile"),
                          keyfile_password=password,
                          ciphers="ECDHE-ECDSA-AES128-GCM-SHA256",
                          tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
            port = 8883

        self.mqttc.user_data_set([])
        self.mqttc.connect("raspberrypi.local", port)
        self.mqttc.loop_forever()
        print(f"Received the following message: {self.mqttc.user_data_get()}")

    def stop_loop(self):
        self.mqttc.loop_stop()

    def on_message(client, userdata, message):
        # userdata is the structure we choose to provide, here it's a list()
        userdata.append(message.payload)
        # if a device is connected, publish the selected cipher
        # so it can start sending measurements
        if message.topic == "device_connected":
            print(f"received device_connected message {message.payload}")
            send_cipher()
        elif message.topic == "measurements":
            print(f"received measurement: {message.payload}")
        #todo save on db

    def on_subscribe(self, userdata, mid, reason_code_list, properties):
        # Since we subscribed only for a single channel, reason_code_list contains
        # a single entry
        if reason_code_list[0].is_failure:
            print(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
        # Be careful, the reason_code_list is only present in MQTTv5.
        # In MQTTv3 it will always be empty
        if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
            print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
        else:
            print(f"Broker replied with failure: {reason_code_list[0]}")
        client.disconnect()

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            client.subscribe("device_connected")
            client.subscribe("measurements")
