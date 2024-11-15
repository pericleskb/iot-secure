import sys
import random
import time
import threading

from interface.mqtt_publisher import MqttPublisher
"""
This file simulates usage from a user
"""
device_name = None

# Check if an argument was passed
if len(sys.argv) != 3:
    print("Please pass the device's name and the private key's encryption passwords as parameters.")
    exit()

device_name = sys.argv[1]
password = sys.argv[2]
mqtt_publisher = MqttPublisher(device_name, password)

def __start_mqtt_publisher():
    mqtt_publisher.start_publishing()

mqtt_publisher_thread = threading.Thread(target=__start_mqtt_publisher)
mqtt_publisher_thread.start()

while True:
    # Generate a random float between 30 and 80
    temperature = random.uniform(20.0, 30.0)
    mqtt_publisher.add_value(temperature)
    time.sleep(5)
