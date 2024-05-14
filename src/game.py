import sys

import pygame

import car
import client
import game_info
from utils import blit_text_center, scale_image

pygame.font.init()


class Game:

    def __init__(self, host, port):
        # Constants/assets
        self.grass = scale_image(pygame.image.load("./assets/grass.jpg"), 2.5)
        self.track = scale_image(pygame.image.load("./assets/track.png"), 0.9)

        self.track_border = scale_image(
            pygame.image.load("./assets/track-border.png"), 0.9
        )
        self.track_border_mask = pygame.mask.from_surface(self.track_border)

        self.finish = pygame.image.load("./assets/finish.png")
        self.finish_mask = pygame.mask.from_surface(self.finish)
        self.finish_position = (130, 250)

        self.max_vel = 4
        self.rotation_vel = 2

        # PLAYER 1 CONSTANTS
        self.red_car = scale_image(pygame.image.load("./assets/red-car.png"), 0.55)
        self.p1_start_pos = (180, 200)

        # PLAYER 2 CONSTANTS
        self.green_car = scale_image(pygame.image.load("./assets/green-car.png"), 0.55)
        self.p2_start_pos = (150, 200)

        # Pygame configs
        self.width, self.height = self.track.get_width(), self.track.get_height()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Socket Speedsters")
        self.main_font = pygame.font.SysFont("comicsans", 44)

        self.game_info = game_info.GameInfo()
        self.client = client.Client(host, port)

        self.cars = [
            car.Car(
                self.max_vel, self.rotation_vel, self.red_car, self.p1_start_pos, 0
            ),
            car.Car(
                self.max_vel, self.rotation_vel, self.green_car, self.p2_start_pos, 1
            ),
        ]

        self.winner = -1

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.images = [
            (self.grass, (0, 0)),
            (self.track, (0, 0)),
            (self.finish, self.finish_position),
            (self.track_border, (0, 0)),
        ]

    def start(self):
        self.game_info.start_game()

        while self.game_info.game_status():
            self.clock.tick(self.fps)
            self.draw()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            if self.game_info.game_status():
                self.move_car()
                self.handle_collision()

            if not self.game_info.game_status():
                blit_text_center(
                    self.window, self.main_font, f"Player {self.winner + 1} won!"
                )
                pygame.display.update()
                pygame.time.wait(10000)

        pygame.quit()

    def draw(self):
        for img, pos in self.images:
            self.window.blit(img, pos)

        for car in self.cars:
            car.draw(self.window)

        pygame.display.update()

    def move_car(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.cars[self.client.id].rotate(left=True)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.cars[self.client.id].rotate(right=True)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            moved = True
            self.cars[self.client.id].move_forward()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            moved = True
            self.cars[self.client.id].move_backward()

        if not moved:
            self.cars[self.client.id].reduce_speed()

        # Send data to server here
        response = self.client.send(self.cars[self.client.id])
        self.cars[response.id].set_abstract_data(response)

    def handle_collision(self):
        if self.cars[self.client.id].collide(self.track_border_mask):
            self.cars[self.client.id].bounce()

        for car in self.cars:
            if car.collide(self.finish_mask, *self.finish_position):
                self.game_info.game_finished()
                self.winner = car.id


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python game.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    game = Game(host, port)
    game.start()
