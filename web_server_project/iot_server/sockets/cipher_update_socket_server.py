import socket

from web_server_project.iot_server.mqtt.ciphers_publisher import send_ciphers

class SocketServer:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.active = True

    def start(self):
        self.server_socket.bind(("127.0.0.1", 8235))
        self.server_socket.listen(1)

        while self.active:
            try:
                self.connection, address = self.server_socket.accept()
                data = self.connection.recv(1024)
                print('Received', data)
                send_ciphers(data)
            #     todo remove b for buffer
            except Exception as e:
                print('Server error', e)
                self.connection.close()
                self.server_socket.close()


    def close(self):
        self.active = False
        self.connection.close()
        self.server_socket.close()