import threading

from mqtt.measurements_subscriber import MeasurementsSubscriber
from sockets.cipher_update_socket_server import SocketServer
from sql.sql_connector import get_selected_option

selected_option = get_selected_option()
print(selected_option)

def start_mqtt_subscriber():
	measurement_subscriber = MeasurementsSubscriber()
	measurement_subscriber.start_subscribe_loop()
	
def start_socket_server():
	socket_server = SocketServer()
	socket_server.start()

mqtt_thread = threading.Thread(target=start_mqtt_subscriber)
socket_thread = threading.Thread(target=start_socket_server)

mqtt_thread.start()
socket_thread.start()

#keep main running until threads finish
mqtt_thread.join()
socket_thread.join()
