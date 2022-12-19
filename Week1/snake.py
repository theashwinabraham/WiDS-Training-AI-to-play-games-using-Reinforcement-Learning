import pygame
from pygame.locals import *

class Square(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Square, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((0, 200, 255))
        # self.rect = self.surf.get_rect()
        self.pos = [x, y]


pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
 
square = Square(40, 40)

# Use blit to put something on the screen
screen.blit(square.surf, tuple(square.pos))

# Update the display using flip
pygame.display.flip()


gameOn = True
# Our game loop
while gameOn:
    # for loop through the event queue
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
    keys = pygame.key.get_pressed()

    print(square.pos)

    square.surf.fill((0, 0, 0))
    screen.blit(square.surf, tuple(square.pos)) # Remove old square
    square.surf.fill((0, 200, 255))
    if keys[K_w] or keys[K_UP]:
        square.pos[1] -= 10
        # keys[K_w] = False
        # keys[K_UP] = False
    elif keys[K_a] or keys[K_LEFT]:
        square.pos[0] -= 10
        # keys[K_a] = False
        # keys[K_LEFT] = False
    elif keys[K_s] or keys[K_DOWN]:
        square.pos[1] += 10
        # keys[K_s] = False
        # keys[K_DOWN] = False
    elif keys[K_d] or keys[K_RIGHT]:
        square.pos[0] += 10
        # keys[K_d] = False
        # keys[K_RIGHT] = False


    square.pos[0] %= W
    square.pos[1] %= H
   


    screen.blit(square.surf, tuple(square.pos)) # Put new square
    # Update the display using flip
    pygame.display.flip()

pygame.quit()