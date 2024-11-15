import sys
import random
import time

from interface.mqtt_publisher import MqttPublisher
from mqtt.device_connected_publisher import send_device_connected

device_name = None

# Check if an argument was passed
if len(sys.argv) != 3:
    print("Please pass the device's name and the private key's encryption passwords as parameters.")
    exit()

device_name = sys.argv[1]
password = sys.argv[2]

mqtt_publisher = MqttPublisher(device_name, password)
mqtt_publisher.start_publishing()

while True:
    # Generate a random float between 30 and 80
    temperature = random.uniform(20.0, 30.0)
    mqtt_publisher.add_value(temperature)
    time.sleep(5)