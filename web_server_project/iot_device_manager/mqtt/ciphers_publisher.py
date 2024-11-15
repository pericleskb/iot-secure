import paho.mqtt.client as mqtt

from files import file_util
from sql.sql_connector import get_selected_option

def send_cipher(password):
    # read selected security cipher suite from db
    selected_cipher = get_selected_option()

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    unacked_publish = set()
    mqttc.on_publish = on_publish

    mqttc.user_data_set(unacked_publish)

    if file_util.should_use_ssl():
        certs = file_util.read_certificate_conf_file()
        # Certificates defined. Use ssl

        mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                           certfile=certs.get("certfile"),
                           keyfile=certs.get("keyfile"),
                           keyfile_password=password,
                           ciphers=selected_cipher,
                           tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
        port = 8883

    mqttc.connect("raspberrypi.local", port)
    mqttc.loop_start()

    msg_info = mqttc.publish("set_cipher_suite", selected_cipher, qos=1)
    print(f"sent message {selected_cipher}")
    unacked_publish.add(msg_info.mid)
    msg_info.wait_for_publish()
    mqttc.disconnect()

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        return
