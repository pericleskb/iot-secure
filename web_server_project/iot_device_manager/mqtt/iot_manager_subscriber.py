import json
from files import file_util
from sql.sql_connector import insert_measurement
from CipherSuites import is_cipher_suite

from mqtt.ciphers_publisher import send_cipher
import paho.mqtt.client as mqtt

"""
    This class implements an MQTT subscriber and will handle all the
    incoming messages from the MQTT broker. 
    It subscribes to 3 topics.
    1. device_connected topic. Each device connected to the network will publish
       a message on this topic and wait to receive the active cipher on the
       set_cipher_suite topic.
    2. measurements topic. Receive the measurements from devices
    3. set_cipher_suite. Receive new security settings
"""
class IotManagerSubscriber:

    def __init__(self, cipher):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.cipher = cipher

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
                          ciphers=self.cipher,
                          tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
            port = 8883

        self.mqttc.user_data_set([])
        self.mqttc.connect("raspberrypi.local", port)
        self.mqttc.loop_forever()
        print(f"Received the following message: {self.mqttc.user_data_get()}")

    def stop_loop(self):
        self.mqttc.loop_stop()

    def on_message(self, client, userdata, message):
        # userdata is the structure we choose to provide, here it's a list()
        userdata.append(message.payload)
        # if a device is connected, publish the selected cipher
        # so it can start sending measurements
        if message.topic == "device_connected":
            print(f"received device_connected message {message.payload}")
            send_cipher()
        elif message.topic == "measurements":
            data = json.loads(message.payload)
            print(f"received measurement: {data}")
            insert_measurement(data["device_name"], data["temperature"])
        elif message.topic == "set_cipher_suite":
            print(
                f"topic: set_cipher_suite, message received - {message.payload}")
            new_cipher = message.payload.decode("utf-8")
            if not is_cipher_suite(new_cipher):
                print(f"Received not supported cipher - {message.payload}")
                return
            if message.payload != self.cipher:
                print("New cipher received")
                self.cipher = new_cipher
                self.stop_loop()
                self.start_subscribe_loop()


    def on_subscribe(self, self1, userdata, mid, reason_code_list, properties):
        #todo check for other reason codes
        if reason_code_list[0].is_failure:
            print(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_unsubscribe(self, self1, client, userdata, mid, reason_code_list, properties):
        if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
            print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
        else:
            print(f"Broker replied with failure: {reason_code_list[0]}")
        client.disconnect()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            client.subscribe("measurements")
            client.subscribe("device_connected")
            client.subscribe("set_cipher_suite")
