from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from socket import error as socketerror

class ValueConnection:

    def __init__(self, ip, port):
        self.address = (ip, port)

    def __enter__(self):
        self.connection = socket(AF_INET, SOCK_DGRAM)
        self.connection.bind(("0.0.0.0", 0))

        return self

    def tell(self, message):
        self.connection.sendto(message, self.address)
        self.connection.settimeout(1.0)
        try:
            self.connection.recvfrom(1)
        except socketerror:
            pass
        self.connection.settimeout(None)

    def __exit__(self, type, value, traceback):
        self.connection.close()

class ControlConnection:

    def __init__(self, ip, port):
        self.address = (ip, port)

    def __enter__(self):
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect(self.address)

        return self

    def order(self, message):
        self.connection.send(message)

    def __exit__(self, type, value, traceback):
        self.connection.close()
