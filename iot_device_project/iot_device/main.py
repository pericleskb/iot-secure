import threading

from mqtt.cipher_subscriber import CipherSubscriber
from mqtt.device_connected_publisher import send_device_connected

def start_cipher_subscriber():
    cipher_subscriber = CipherSubscriber()
    cipher_subscriber.start_subscribe_loop()

# start cipher subscriber in different thread to not block current execution
# this subscriber will handle the measurements publisher
cipher_subscriber_thread = threading.Thread(target=start_cipher_subscriber)
cipher_subscriber_thread.start()

# publish device connected message, so that the server can respond with
# the active cipher in cipher_subscriber
send_device_connected()

# join to get print results
cipher_subscriber_thread.join()
