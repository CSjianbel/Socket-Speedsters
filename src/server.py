import socket

from utils import scale_image, blit_text_center
from game import game_info, car

pygame.font.init()

GRASS = scale_image(pygame.image.load("../assets/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("../assets/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("../assets/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("../assets/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

# PLAYER 1 CONSTANTS
RED_CAR = scale_image(pygame.image.load("../assets/red-car.png"), 0.55)
P1_START_POS = (180, 200)

# PLAYER 1 CONSTANTS
GREEN_CAR = scale_image(pygame.image.load("../assets/green-car.png"), 0.55)
P1_START_POS = (150, 200)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60

game_info = game_info.GameInfo()

def handle_client(conn, player):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            print("Player", player, "disconnected")
            break
        print("Received from Player", player, ":", data)
        # Process received data, implement game logic here
        # Send response to the other player
        other_player = 2 if player == 1 else 1
        other_conn.sendall(data.encode())

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 8888)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(2)

print("Waiting for two players...")

# Accept connections from two players
conn1, addr1 = sock.accept()
print("Player 1 connected from", addr1)
conn2, addr2 = sock.accept()
print("Player 2 connected from", addr2)

# Start handling the game for each player in separate threads or processes
# You can use threading or multiprocessing modules for this purpose
# For simplicity, let's handle each player in the main thread for now
handle_client(conn1, 1)
handle_client(conn2, 2)

# Close the main listening socket
sock.close()

