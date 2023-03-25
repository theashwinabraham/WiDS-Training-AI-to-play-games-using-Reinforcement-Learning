import pygame
from pygame.locals import *
from random import randrange


size = 20
sep = size
last_key = 'r'
n = 3



class Square(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Square, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill((0, 200, 255))
        # self.rect = self.surf.get_rect()
        self.pos = [x, y]
        self.current_direction = 'r'
        self.next_direction = None


def remove_snake(square):
    for s in range(len(square)):
        square[s].surf.fill((0, 0, 0))
        screen.blit(square[s].surf, tuple(square[s].pos)) # Remove old square
        if s == 0:
            square[s].surf.fill((255, 0, 0))
        else:
            square[s].surf.fill((0, 200, 255))

def put_snake(square):
    for s in square:
        screen.blit(s.surf, tuple(s.pos)) # Put new square

def update_snake(square, last_key):

    square[0].current_direction = last_key

    for i in range(1, len(square)):
        square[i].next_direction = square[i-1].current_direction
    

    for s in square:
        if s.current_direction == 'u':
            s.pos[1] -= size
        elif s.current_direction == 'd':
            s.pos[1] += size
        elif s.current_direction == 'r':
            s.pos[0] += size
        elif s.current_direction == 'l':
            s.pos[0] -= size

    for i in range(1, len(square)):
        if square[i].pos[0]%size == 0 or square[i].pos[1]%size == 0:
            square[i].current_direction = square[i].next_direction

def check_eat(square):
    global gameOn
    for i in range(2, len(square)):
        if (square[0].pos[0] == square[i].pos[0]) and (square[0].pos[1] == square[i].pos[1]):
            print("now")
            gameOn = False
    if square[0].pos[0] == size*-1 or square[0].pos[0] == 800 or square[0].pos[1] == size*-1 or square[0].pos[1] == 600:
        gameOn = False

def add_tail(square):
    square.append(Square(square[len(square) - 1].pos[0] - size, square[len(square) - 1].pos[1]))

pygame.init()

screen = pygame.display.set_mode((800, 600))
 
square = [Square(size-sep*i, size) for i in range(n)]
square[0].surf.fill((255, 0, 0))

put_snake(square)

pygame.display.flip()

box = Square(randrange(800/size-size)*size, randrange(600/size-size)*size)
box.surf.fill((255,255,255))

gameOn = True

while gameOn:


    if square[0].pos[0] == box.pos[0] and square[0].pos[1] == box.pos[1]:
        add_tail(square)
        box.surf.fill((0, 0, 0))

        box.pos[0] = randrange(800/size-size)*size
        box.pos[1] = randrange(600/size-size)*size

        screen.blit(box.surf, tuple(box.pos))
        box.surf.fill((255,255,255))


    # for loop through the event queue
    pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
    keys = pygame.key.get_pressed()
    remove_snake(square)
    if (keys[K_w] or keys[K_UP]) and last_key != 'd':
        last_key = 'u'
    elif keys[K_a] or keys[K_LEFT] and last_key != 'r':
        last_key = 'l' 
    elif keys[K_s] or keys[K_DOWN] and last_key != 'u':
        last_key = 'd'
    elif keys[K_d] or keys[K_RIGHT] and last_key != 'l':
        last_key = 'r'
    
    update_snake(square, last_key)
    screen.blit(box.surf, tuple(box.pos))


    put_snake(square)

    pygame.display.flip()

    check_eat(square)

pygame.quit()