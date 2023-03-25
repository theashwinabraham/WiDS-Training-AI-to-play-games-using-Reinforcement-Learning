import pygame
from pygame.locals import *

from random import randint


sq_size = 20
obj_size = sq_size*1.0
move_size = sq_size*1.0

cyan = (0, 200, 255)
red = (255, 0, 0)
green = (83, 237, 86)

class Square(pygame.sprite.Sprite):

    def __init__(self, x, y, sq_size, colour):
        super(Square, self).__init__()
        self.size = sq_size
        self.colour = colour
        self.surf = pygame.Surface((sq_size, sq_size))
        self.surf.fill(colour)
        self.pos = [x, y]


pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
obj = Square(W/2, H/2, obj_size, green)
 
count = 3
square = [Square(40, 40, sq_size, cyan) for _ in range(count)]

dirn = [0]*(count+1)

move = {
    0 : [0, -move_size],
    1 : [-move_size, 0],
    2 : [0, move_size],
    3 : [move_size, 0]
}

def move_head():
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        dirn.append(0)
    elif keys[K_a] or keys[K_LEFT]:
        dirn.append(1)
    elif keys[K_s] or keys[K_DOWN]:
        dirn.append(2)
    elif keys[K_d] or keys[K_RIGHT]:
        dirn.append(3)
    else:
        dirn.append(dirn[-1])

    if abs(dirn[-1] - dirn[-2]) == 2:
        del dirn[-1]

    square[0].pos = [square[0].pos[j] + move[dirn[-1]][j] for j in [0, 1]]
        
    square[0].pos[0] %= W
    square[0].pos[1] %= H

def remove_prev():
    for i in range(count):
        square[i].surf.fill((0, 0, 0))
        screen.blit(square[i].surf, tuple(square[i].pos)) # Remove old square[i]
        square[i].surf.fill((0, 200, 255))
    square[0].surf.fill((255, 0, 0))

def move_tail():
    for i in range(1, count):
        square[i].pos = [square[i-1].pos[j] - move[dirn[-i]][j] for j in [0, 1]]
        square[i].pos[0] %= W
        square[i].pos[1] %= H

def display_all():
    for i in range(count):
        screen.blit(square[i].surf, tuple(square[i].pos)) # Put new square[i]

def check_crash():
    global gameOn
    for i in range(1, count):
        if square[0].pos == square[i].pos:
            gameOn = False
            break

def check_touch(a, b):
    dist = [a.pos[i] - b.pos[i] for i in [0, 1]]
    err = 1e-3
    return (abs(dist[0]) < err and abs(dist[1]) < err)

def gen_obj():
    x = randint(sq_size, W - sq_size)
    x -= x%sq_size
    y = randint(sq_size, H - sq_size)
    y -= y%sq_size
    obj.pos = [x, y]
    obj.surf.fill(green)
    screen.blit(obj.surf, tuple(obj.pos))

# Use blit to put something on the screen
screen.blit(obj.surf, tuple(obj.pos))
screen.blit(square[0].surf, tuple(square[0].pos))

# Update the display using flip
pygame.display.flip()


gameOn = True
# Our game loop
while gameOn:
    square[0].surf.fill(red)
    # for loop through the event queue
    pygame.time.Clock().tick(60)
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
    

    #print(square[0].pos, obj.pos, dirn[-5:])

    remove_prev()

    move_head()

    move_tail()

    display_all()
    
    check_crash()

    if check_touch(square[0], obj):
        obj.surf.fill((0, 0, 0))
        screen.blit(obj.surf, tuple(obj.pos)) # Remove old obj
        count += 1
        square.append(Square(square[-1].pos[0], square[-1].pos[1], sq_size, cyan))
        gen_obj()


    # Update the display using flip
    pygame.display.flip()

pygame.time.wait(1000)
pygame.quit()