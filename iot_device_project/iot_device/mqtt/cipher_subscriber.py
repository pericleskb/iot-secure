import paho.mqtt.client as mqtt

from ..files import file_util

class CipherSubscriber:

    def __init__(self):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        

    def start_subscribe_loop(self):
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message
        self.mqttc.on_subscribe = on_subscribe
        self.mqttc.on_unsubscribe = on_unsubscribe

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


    def stop_loop(self):
        self.mqttc.loop_stop()



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

def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    userdata.append(message.payload)
    print(f"message received {message.payload}")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("set_cipher_suite")
