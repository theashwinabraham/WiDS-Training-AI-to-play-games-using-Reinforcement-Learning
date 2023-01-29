import numpy as np
import pygame
from pygame.locals import *

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

class Square(pygame.sprite.Sprite):

    def __init__(self, x, y, color):
        super(Square, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill(color)
        # self.rect = self.surf.get_rect()
        self.pos = [x, y]

    def check_intx(self, sq) : 

        if np.abs(self.pos[0] - sq.pos[0]) < 20 and np.abs(self.pos[1] - sq.pos[1]) < 20 : 
            return True
        else : 
            return False

class Snake :

    def __init__(self, x, y) : 
        pygame.init()
        self.gameOn = True
        self.blocks = [Square(x, y, blue)]
        self.dimensions = (800, 600)
        self.padding = 20
        self.screen = pygame.display.set_mode(self.dimensions)
        self.hit = False
        self.score = 0
        self.food_score = 10
        self.up, self.left, self.right, self.down = False, False, False, False

        # Use blit to put something on the screen
        self.screen.blit(self.blocks[0].surf, tuple(self.blocks[0].pos))
        self.length = 1
        self.add_food()

        # Update the display using flip
        pygame.display.flip()
        

    def delete_tail(self) : 

        self.blocks[-1].surf.fill(black)
        self.screen.blit(self.blocks[-1].surf, tuple(self.blocks[-1].pos))
        self.blocks = self.blocks[:-1]

    def add_head(self, x, y) : 
        
        if x >= self.dimensions[0] : x -= self.dimensions[0]
        if x < 0 : x += self.dimensions[0]
        if y >= self.dimensions[1] : y-= self.dimensions[1]
        if y < 0 : y += self.dimensions[1]


        head = [Square(x, y, blue)]
        self.screen.blit(head[0].surf, tuple(head[0].pos))

        head.extend(self.blocks)
        self.blocks = head

    def del_food(self) : 
        self.food.surf.fill(black)
        self.screen.blit(self.food.surf, tuple(self.food.pos))
        self.score += self.food_score

    def add_food(self) : 

        self.food_x, self.food_y = np.random.randint(self.padding, self.dimensions[0]-self.padding), np.random.randint(self.padding, self.dimensions[1] - self.padding)
        self.food = Square(self.food_x, self.food_y, yellow)
        self.screen.blit(self.food.surf, tuple(self.food.pos))

    def check_loss(self) : 

        for i in self.blocks[1:] :
            if i.check_intx(self.blocks[0]) : 
                return True
        
        return False

    def update_pos(self) : 
        [x, y] = self.blocks[0].pos
        if self.up or self.keys[K_UP]:
            if self.down and self.length != 1 : self.gameOn = False
            self.up, self.down, self.right, self.left = True, False, False, False
            y -= 20
        if self.left or self.keys[K_LEFT]:
            if self.right and self.length != 1 : self.gameOn = False
            self.up, self.down, self.right, self.left = False, False, False, True
            x -= 20
        if self.down or self.keys[K_DOWN]:
            if self.up and self.length != 1 : self.gameOn = False
            self.up, self.down, self.right, self.left = False, True, False, False
            y += 20
        if self.right or self.keys[K_RIGHT]:
            if self.left and self.length != 1 : self.gameOn = False
            self.up, self.down, self.right, self.left = False, False, True, False
            x += 20
        if [x,y] != self.blocks[0].pos : 
            if not self.hit : 
                self.delete_tail()
            else : 
                self.length += 1
                self.hit = False
            self.add_head(x, y)
            if self.check_loss() : 
                self.gameOn = False

    def print_score(self) : 
        print("Score : ",self.score)

    def gameLoop(self) : 
        # Our game loop
        while self.gameOn:

            while self.length > len(self.blocks) : 
                self.blocks = self.blocks[:-1]

            # for loop through the event queue
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.gameOn = False
            
            self.keys = pygame.key.get_pressed()
            
            if np.abs(self.blocks[0].pos[0]-self.food.pos[0]) <= 20 and  np.abs(self.blocks[0].pos[1]-self.food.pos[1]) <= 20: 
                self.del_food()
                self.hit = True
                self.add_food()
            self.update_pos()

            #print(self.blocks[0].pos)
            # Update the display using flip
            pygame.display.flip()

        self.print_score()
        pygame.quit()

snake = Snake(20, 20)
snake.gameLoop()
