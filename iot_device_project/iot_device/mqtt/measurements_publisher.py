import json
import paho.mqtt.client as mqtt

from files import file_util

class MeasurementsPublisher:

    def __init__(self, cipher, device_name, password, queue):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.cipher = cipher
        self.device_name = device_name
        self.password = password
        self.value_queue = queue
        self.unacked_publish = set()

    def start_loop(self):
        self.mqttc.on_publish = on_publish

        self.mqttc.user_data_set(self.unacked_publish)
        port = 1883

        if file_util.should_use_ssl():
            # Certificates defined. Use ssl
            certs = file_util.read_certificate_conf_file()

            self.mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                          certfile=certs.get("certfile"),
                          keyfile=certs.get("keyfile"),
                          keyfile_password=self.password,
                          ciphers=self.cipher,
                          tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
            port = 8883

        self.mqttc.connect("raspberrypi.local", port)
        self.mqttc.loop_start()

    def stop_loop(self):
        self.mqttc.loop_stop()

    def add_value(self, value):
        data = {
            "device_name": self.device_name,
            "temperature": value
        }
        msg_info = self.mqttc.publish("measurements", json.dumps(data),
                                      qos=1)
        print(f"sent message {json.dumps(data)}")
        self.unacked_publish.add(msg_info.mid)
        msg_info.wait_for_publish()

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        return
