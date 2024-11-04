from mqtt.measurements_subscriber import MeasurementsSubscriber
from sockets.cipher_update_socket_server import SocketServer
from sql.sql_connector import get_selected_option

selected_option = get_selected_option()
print(selected_option)

measurement_subscriber = MeasurementsSubscriber()
measurement_subscriber.start_subscribe_loop()

socket_server = SocketServer()
socket_server.start()

