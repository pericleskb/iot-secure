import time
import random
import json
import paho.mqtt.client as mqtt

from files import file_util

class MeasurementsPublisher:

    def __init__(self, cipher, device_name, password):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.cipher = cipher
        self.device_name = device_name
        self.password = password

    def start_loop(self):
        unacked_publish = set()
        self.mqttc.on_publish = on_publish

        self.mqttc.user_data_set(unacked_publish)
        port = 1883

        if file_util.should_use_ssl():
            # Certificates defined. Use ssl
            certs = file_util.read_certificate_conf_file()

            self.mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                          certfile=certs.get("certfile"),
                          keyfile=certs.get("keyfile"),
                          keyfile_password=self.password,
                          ciphers=self.cipher,
                          tls_version=CipherSuites.get_description(selected_cipher))
            port = 8883

        self.mqttc.connect("raspberrypi.local", port)
        self.mqttc.loop_start()

        while True:
            # Generate a random float between 30 and 80
            temperature = random.uniform(30.0, 80.0)
            data = {
                "device_name": self.device_name,
                "temperature": temperature
            }
            msg_info = self.mqttc.publish("measurements", json.dumps(data), qos=1)
            print(f"sent message {json.dumps(data)}")
            unacked_publish.add(msg_info.mid)
            msg_info.wait_for_publish()
            time.sleep(20)


    def stop_loop(self):
        self.mqttc.loop_stop()


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")
