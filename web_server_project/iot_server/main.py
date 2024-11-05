import threading

from mqtt.iot_manager_subscriber import IotManagerSubscriber
from mqtt.ciphers_publisher import send_cipher
from sockets.cipher_update_socket_server import SocketServer

def start_iot_manager_subscriber():
	measurement_subscriber = IotManagerSubscriber()
	measurement_subscriber.start_subscribe_loop()

def start_socket_server():
	socket_server = SocketServer()
	socket_server.start()

mqtt_thread = threading.Thread(target=start_iot_manager_subscriber)

# start IPC socket to be able to receive messages about
# changes on the selected cipher
socket_thread = threading.Thread(target=start_socket_server)

mqtt_thread.start()
socket_thread.start()

# publish selected cipher in case there are iot devices already connected to
# the network
send_cipher()

#keep main running until threads finish
mqtt_thread.join()
socket_thread.join()
