# Importing Libraries
import pygame
from pygame.locals import *
import random
import os

# Initialized pygame
pygame.init()

# Defining the class Square


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super(Square, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill(color)
        self.pos = [x, y]


# Game variables
screen_height = 900
screen_width = 600
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Snake")
square = Square(40, 40, (0, 200, 255))
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()

pygame.display.update()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
cyan = (0, 200, 255)


# Game Functions
def plot_snake(screen, snk_list, color, size):
    for pos in snk_list:
        pygame.draw.rect(screen, color, (pos[0], pos[1], size, size))


def text_display(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

# Welcome window


def welcome():
    exit_game = False
    while not exit_game:
        screen.fill((233, 210, 229))
        text_display("Welcome to Snakes", black, 260, 250)
        text_display("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

# Game loop


def game_loop():
    # Game instance variables
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 50
    init_vel = 5
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    snake_size = 20
    snake_length = 1
    snake_list = []
    score = 0
    fps = 60

    # Load the high_scores
    if not os.path.exists("hi_score.txt"):
        with open("hi_score.txt", "w") as f:
            f.write("0")

    with open("hi_score.txt", "r") as f:
        hi_score = f.read()

    while not exit_game:
        # for loop through the event queue
        if game_over:
            screen.fill(black)
            text_display("Game Over, Return to Home", red, 200, 250)
            with open("hi_score.txt", "w") as f:
                f.write(hi_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = True
            keys = pygame.key.get_pressed()

            if keys[K_w] or keys[K_UP] and velocity_y==0:
                velocity_x = 0
                velocity_y = -init_vel
            if keys[K_a] or keys[K_LEFT] and velocity_x==0:
                velocity_x = -init_vel
                velocity_y = 0
            if keys[K_s] or keys[K_DOWN] and velocity_y==0:
                velocity_x = 0
                velocity_y = init_vel
            if keys[K_d] or keys[K_RIGHT] and velocity_x==0:
                velocity_x = init_vel
                velocity_y = 0
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                if score > int(hi_score):
                    hi_score = str(score)
                food_x = random.randint(20, screen_width/1.5)
                food_y = random.randint(20, screen_height/1.5)
                snake_length += 5

            head = Square(snake_x, snake_y, cyan)
            snake_list.append(head.pos)

            if snake_length < len(snake_list):
                del snake_list[0]

            if snake_x <= 0 or snake_x >= screen_width or snake_y <= 0 or snake_y >= screen_height:
                game_over = True

            if head.pos in snake_list[:-1]:
                game_over = True

            screen.fill(black)
            text_display("Score: " + str(score) +
                         "  High Score: " + hi_score, red, 5, 5)
            pygame.draw.rect(screen, red,
                             (food_x, food_y, snake_size, snake_size))
            plot_snake(screen, snake_list, cyan, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


# Main
if __name__ == '__main__':
    welcome()
