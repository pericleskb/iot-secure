import socket

from mqtt.ciphers_publisher import send_ciphers

"""
    The SocketServer receives messages about changes the user makes on the 
    selected cipher suite. Each time a change is detected, we need to publish
    the change using the ciphers_publisher
"""
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
                send_ciphers()
            #     todo remove b for buffer
            except Exception as e:
                print('Server error', e)
                self.connection.close()
                self.server_socket.close()


    def close(self):
        self.active = False
        self.connection.close()
        self.server_socket.close()
