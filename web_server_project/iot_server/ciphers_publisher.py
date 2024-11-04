import paho.mqtt.client as mqtt

import file_util

def send_ciphers(cipher):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    unacked_publish = set()
    mqttc.on_publish = on_publish

    mqttc.user_data_set(unacked_publish)

    if file_util.should_use_ssl():
        certs = file_util.read_certificate_conf_file()
        # Certificates defined. Use ssl

        password = certs.get("password") if certs.get("password") else None

        mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                           certfile=certs.get("certfile"),
                           keyfile=certs.get("keyfile"),
                           keyfile_password=password,
                           ciphers="ECDHE-ECDSA-AES128-GCM-SHA256",
                           tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
        port = 8883

    mqttc.connect("raspberrypi.local", port)
    print("connected")

    msg_info = mqttc.publish("set_cipher_suite", cipher, qos=1)
    print(f"sent message {cipher}")
    unacked_publish.add(msg_info.mid)
    msg_info.wait_for_publish()


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
