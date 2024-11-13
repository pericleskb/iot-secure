import threading
import sys

from mqtt.cipher_subscriber import CipherSubscriber
from mqtt.device_connected_publisher import send_device_connected

device_name = None

def start_cipher_subscriber():
    cipher_subscriber = CipherSubscriber(device_name)
    cipher_subscriber.start_subscribe_loop()

# Check if an argument was passed
if len(sys.argv) != 2:
    print("Please pass the device's name as a parameter.")
    exit()

device_name = sys.argv[1]

# start cipher subscriber in different thread to not block current execution
# this subscriber will handle the measurements publisher
cipher_subscriber_thread = threading.Thread(target=start_cipher_subscriber)
cipher_subscriber_thread.start()

# publish device connected message, so that the server can respond with
# the active cipher in cipher_subscriber
# If the IoT Device Manager is not running during this time, it will publish
# the active cipher at the time of its connection
send_device_connected()

# join to get print results
cipher_subscriber_thread.join()
