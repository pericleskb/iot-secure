import paho.mqtt.client as mqtt
import os

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

def read_certificate_conf_file(file_path):
    """The paths of the SSL certificates and keys are needed to use SSL.
        It is unsafe to store this in the code, so they must be stored
        separately on the machine that will run the MQTT client.
        The MQTT client needs to be provided with the path to these files.
        Instead of using a standard path for each file, we use a standard path
        for the configuration file and the files can be stored wherever the user
        wishes. The format of the file should be
        key=path
        key=path
    """

    # Dictionary to store key-value pairs
    certs = {}

    # Open the file and read it line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by '=' to separate key and value
            key_value = line.strip().split('=')

            # Check if the line contains exactly two elements (key and value)
            if len(key_value) == 2:
                key, value = key_value
                # Store the key-value pair in the dictionary
                certs[key.strip()] = value.strip()
    return certs


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# get OS independent home path
home_dir = os.path.expanduser("~")
# using OS independent path separator to create path /home/ssl/certificates.conf
certs = read_certificate_conf_file(
    home_dir + os.sep + "ssl" + os.sep + "certificates.conf"
)
if len(certs) != 0:
    #Certificates defined. Use ssl
    mqttc.tls_set(ca_certs = certs.get("ca_certs"),
                  certfile = certs.get("ca_certs"),
                  keyfile= certs.get("keyfile"))

mqttc.user_data_set([])
mqttc.connect("mqtt.eclipseprojects.io")
mqttc.loop_forever()
print(f"Received the following message: {mqttc.user_data_get()}")
