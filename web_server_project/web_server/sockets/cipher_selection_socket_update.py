import socket

def update_cipher(cipher):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8235))
    client_socket.sendall(cipher.encode('utf-8'))
    client_socket.shutdown(socket.SHUT_RDWR)
