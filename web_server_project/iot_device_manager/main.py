import ssl
import threading
import sys
import queue

from mqtt.iot_manager_subscriber import IotManagerSubscriber
from mqtt.ciphers_publisher import send_cipher
from sockets.cipher_update_socket_server import SocketServer
from sql.sql_connector import get_selected_option

# Check if an argument was passed
if len(sys.argv) != 2:
	print(
		"Please pass the private key's encryption passwords as a parameter.")
	exit()

password = sys.argv[1]
selected_option = get_selected_option()

def start_iot_manager_subscriber(q):
	measurement_subscriber = IotManagerSubscriber(q, selected_option, password)
	measurement_subscriber.start_subscribe_loop()

def start_socket_server():
	socket_server = SocketServer(password)
	socket_server.start()

# create queue to get result from iot manager thread
q = queue.Queue()
mqtt_thread = threading.Thread(target=start_iot_manager_subscriber, args=(q,))

# start IPC socket to be able to receive messages about
# changes on the selected cipher
socket_thread = threading.Thread(target=start_socket_server)

mqtt_thread.start()
socket_thread.start()

# publish selected cipher in case there are iot devices already connected to
# the network
try:
	send_cipher(password)
except ssl.SSLError:
	print("Unable to connect. "
		  "Please make sure you provided the correct password.")
	SystemExit(1)

# keep main running until new cipher is received, when the thread will
# stop itself
mqtt_thread.join()

# Retrieve the result from the queue
result = q.get()

# if no exit result was provided
# get new option from database and restart thread with new cipher
while result != -1:
	selected_option = get_selected_option()
	mqtt_thread.start()
	mqtt_thread.join()
	result = q.get()
