import pygame

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

def draw(win, images, player1_car, player2_car):
    for img, pos in images:
        win.blit(img, pos)
    player1_car.draw(win)
    player2_car.draw(win)
    pygame.display.update()


def move_car(player_car, player_num):
    keys = pygame.key.get_pressed()
    moved = False

    if (player_num == 1 and keys[pygame.K_a]) or (player_num == 2 and keys[pygame.K_LEFT]):
        player_car.rotate(left=True)
    if (player_num == 1 and keys[pygame.K_d]) or (player_num == 2 and keys[pygame.K_RIGHT]):
        player_car.rotate(right=True)
    if (player_num == 1 and keys[pygame.K_w]) or (player_num == 2 and keys[pygame.K_UP]):
        moved = True
        player_car.move_forward()
    if (player_num == 1 and keys[pygame.K_s]) or (player_num == 2 and keys[pygame.K_DOWN]):
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, player_num, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, f"Player {player_num} won!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player1_car = car.Car(4, 4, RED_CAR, (180, 200))
player2_car= car.Car(2, 4, GREEN_CAR, (150, 200))
game_info = game_info.GameInfo()

while run:
    clock.tick(FPS)

    draw(WIN, images, player1_car, player2_car)

    while not game_info.started:
        blit_text_center(
            WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_car(player1_car, 1)
    move_car(player2_car, 2)

    handle_collision(player1_car, 1, player2_car, game_info)
    handle_collision(player2_car, 2, player1_car, game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You won the game!")
        pygame.time.wait(5000)
        game_info.reset()
        player1_car.reset()
        player2_car.reset()


pygame.quit()
