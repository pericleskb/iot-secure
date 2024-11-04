from mqtt.measurements_subscriber import MeasurementsSubscriber
from sockets.cipher_update_socket_server import SocketServer



measurement_subscriber = MeasurementsSubscriber()
measurement_subscriber.start_subscribe_loop()

socket_server = SocketServer()
socket_server.start()

