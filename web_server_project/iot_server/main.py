from measurements_subscriber import MeasurementsSubscriber
from web_server_project.iot_server.cipher_update_socket_server import \
    SocketServer

measurement_subscriber = MeasurementsSubscriber()
measurement_subscriber.start_subscribe_loop()

socket_server = SocketServer()
socket_server.start()

