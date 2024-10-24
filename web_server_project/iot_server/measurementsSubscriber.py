import os
import paho.mqtt.client as mqtt

from web_server_project.iot_server import file_util


class MeasurementsSubscriber:

    def start_subscribe_loop(self):
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.on_subscribe = on_subscribe
        mqttc.on_unsubscribe = on_unsubscribe

        port = 1883

        # get OS independent home path
        home_dir = os.path.expanduser("~")
        # using OS independent path separator to create path /home/ssl/certificates.conf
        certs = file_util.read_certificate_conf_file(
            home_dir + os.sep + "ssl" + os.sep + "certificates.conf"
        )
        if file_util.should_use_ssl(certs):
            print(certs.get("ca_certs"))
            print(certs.get("certfile"))
            print(certs.get("keyfile"))
            print(certs.get("passwordfile"))
            # Certificates defined. Use ssl

            password = file_util.get_password(certs.get("passwordfile")) if certs.get("passwordfile") else None

            mqttc.tls_set(ca_certs=certs.get("ca_certs"),
                          certfile=certs.get("certfile"),
                          keyfile=certs.get("keyfile"),
                          keyfile_password=password,
                          tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
            port = 8883

        mqttc.user_data_set([])
        mqttc.connect("raspberrypi.local", port)
        mqttc.loop_forever()
        print(f"Received the following message: {mqttc.user_data_get()}")

def on_subscribe(client, userdata, mid, reason_code_list, properties):
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
    #todo save on db

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("measurements")