import time
import random
import os
import paho.mqtt.client as mqtt

class Publisher:

    def startLoop(self):
        unacked_publish = set()
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_publish = on_publish

        mqttc.user_data_set(unacked_publish)

        # get OS independent home path
        home_dir = os.path.expanduser("~")
        # using OS independent path separator to create path /home/ssl/certificates.conf
        certs = read_certificate_conf_file(
            home_dir + os.sep + "ssl" + os.sep + "certificates.conf")
        if len(certs) != 0:
            #Certificates defined. Use ssl
            mqttc.tls_set(ca_certs = certs.get("ca_certs"), certfile = certs.get("ca_certs"), keyfile= certs.get("keyfile"))

        mqttc.connect("mqtt.eclipseprojects.io")
        print("connected")
        mqttc.loop_start()
        print("loop started")

        while True:
            # Generate a random float between 30 and 80
            temperature = random.uniform(30.0, 80.0)
            msg_info = mqttc.publish("measurements", temperature, qos=1)
            print(f"sent message {temperature}")
            unacked_publish.add(msg_info.mid)
            msg_info.wait_for_publish()
            time.sleep(5)


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

