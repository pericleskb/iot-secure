import ssl

import paho.mqtt.client as mqtt

from files import file_util

def send_device_connected(password):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    unacked_publish = set()
    mqttc.on_publish = on_publish

    mqttc.user_data_set(unacked_publish)

    if file_util.should_use_ssl():
        certs = file_util.read_certificate_conf_file()
        # Certificates defined. Use ssl

        try:
            # use default cipher suite for first message
            mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                               certfile=certs.get("certfile"),
                               keyfile=certs.get("keyfile"),
                               keyfile_password=password,
                               ciphers="ECDHE-ECDSA-AES256-GCM-SHA384",
                               tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
            port = 8883
        except ssl.SSLError:
            quit()

    mqttc.connect("raspberrypi.local", port)
    mqttc.loop_start()
    msg_info = mqttc.publish("device_connected", "", qos=1)

    unacked_publish.add(msg_info.mid)
    msg_info.wait_for_publish()
    mqttc.disconnect()


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        return
