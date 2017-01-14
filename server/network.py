from socket import socket, AF_INET, SOCK_DGRAM
from socket import error as socketerror

class Network:

    def __init__(self, ip, port):
        self.address = (ip, port)

    def __enter__(self):
        self.network = socket(AF_INET, SOCK_DGRAM)
        self.network.bind(("0.0.0.0", 0))

        return self

    def tell(self, message):
        self.network.sendto(message, self.address)
        self.network.settimeout(1.0)
        try:
            self.network.recvfrom(1)
        except socketerror:
            pass
        self.network.settimeout(None)

    def __exit__(self, type, value, traceback):
        self.network.close()
