import pickle
import socket
import threading


class Server:
    def __init__(self):
        self.host = "0.0.0.0"  # Listen on all available network interfaces
        self.port = 9999
        self.max_connections = 2
        self.current_connections = 0
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.p1_start_pos = (180, 200)
        self.p2_start_pos = (150, 200)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_connections)
        ip = socket.gethostbyname(socket.gethostname())
        print(f"Server is listening for connections on {ip}:{self.port}...")
        while True:
            client_socket, address = self.server_socket.accept()
            if self.current_connections < self.max_connections:
                self.current_connections += 1
                print(f"Connection from {address} accepted.")
                client_handler = threading.Thread(
                    target=self.handle_client, args=(client_socket,)
                )
                client_handler.start()
                self.clients.append(client_socket)
                if self.current_connections == self.max_connections:
                    print("Maximum number of connections reached. Game can start now.")
            else:
                print(
                    "Maximum number of connections reached. Rejecting new connection."
                )
                client_socket.close()

    def handle_client(self, client_socket):
        client_socket.send(str.encode(str(self.current_connections - 1)))
        while True:
            try:
                message = client_socket.recv(1024)
                print("Received:", message)
                if message:
                    car = pickle.loads(message)
                    self.broadcast(car)
            except Exception as e:
                print("Error occurred:", e)
                break

        client_socket.close()
        self.current_connections -= 1
        print("Client disconnected.")

    def broadcast(self, car):
        for client in self.clients:
            try:
                client.sendall(pickle.dumps(car))
            except Exception as e:
                print("Error broadcasting message to client:", e)


if __name__ == "__main__":
    server = Server()
    server.start()
