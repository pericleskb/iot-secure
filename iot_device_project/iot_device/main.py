import threading
import sys

from mqtt.cipher_subscriber import CipherSubscriber
from mqtt.device_connected_publisher import send_device_connected

def start_cipher_subscriber(name):
    cipher_subscriber = CipherSubscriber(name)
    cipher_subscriber.start_subscribe_loop()

# Check if an argument was passed
if len(sys.argv) != 1:
    print("Please pass the device's name as a parameter.")
    exit()

device_name = sys.argv[1]

# start cipher subscriber in different thread to not block current execution
# this subscriber will handle the measurements publisher
cipher_subscriber_thread = threading.Thread(target=start_cipher_subscriber(device_name))
cipher_subscriber_thread.start()
# publish device connected message, so that the server can respond with
# the active cipher in cipher_subscriber
send_device_connected()
# join to get print results
cipher_subscriber_thread.join()
