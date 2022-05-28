#import pygame and neat-python
import enum
import pygame
import neat
import os
import random
import sys


# make the dino chrome game
pygame.init()

# set screen height and width
HEIGHT = 600
WIDTH = 1100

# create a screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
 
# import the images of the dinosaur running and jumping from the assets folder
RUNNING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))]
JUMPING = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))


# import the background from the assets folder
BG = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))

# import the images of the cactus and the ground from the assets folder
# CACTUS = pygame.image.load(os.path.join('Assets/Cactus', 'Cactus.png'))

# import a font
FONT = pygame.font.SysFont('comicsans', 30)


class Dinosaur():
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL    
        self.step_index = 0

        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.image.get_width(), self.image.get_height())

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        if self.jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run= True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = RUNNING[self.step_index//5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

def main():
    clock = pygame.time.Clock()
    dinosaurs = [Dinosaur()]

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        SCREEN.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        user_input = pygame.key.get_pressed()

        for i, dinosaur in enumerate(dinosaurs):
            if user_input[pygame.K_SPACE]:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        clock.tick(30)
        pygame.display.update()

main()
  