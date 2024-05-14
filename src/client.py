import pickle
import socket


class Client:

    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.id = int(self.connect())

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(pickle.dumps(data.get_abstract_data()))
            response = pickle.loads(self.client.recv(2048))
            return response
        except socket.error as e:
            return str(e)
