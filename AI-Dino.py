import pygame
import os
import random
import math
import sys
import neat
import glob 
import visualize


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

SMALL_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus1.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus3.png'))]
LARGE_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus1.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus3.png'))]



# import the background from the assets folder
BG = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))

# import the images of the cactus and the ground from the assets folder
# CACTUS = pygame.image.load(os.path.join('Assets/Cactus', 'Cactus.png'))

# import a font
FONT = pygame.font.SysFont('comicsans', 20)

checkpointer = neat.Checkpointer()

class Dinosaur():
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.big_jump = True
        self.jump_vel = self.JUMP_VEL    
        self.step_index = 0
        self.color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

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
        if self.dino_jump and self.big_jump == True:
            self.rect.y -= self.jump_vel * 4.5
            self.jump_vel -= 0.8
        elif self.dino_jump and self.big_jump == False:
            self.rect.y -= self.jump_vel * 3.5
            self.jump_vel -= 1
        
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
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)

class Obstacle():
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300

def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2 + dy**2)


def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, dinosaurs, obstacles, ge, nets, points, best_genome_current_gen

    clock = pygame.time.Clock()
    points = 0

    dinosaurs = []
    obstacles = []
    ge = []
    nets = []

    best_genome_current_gen = neat.DefaultGenome(None)
    best_genome_current_gen.fitness = -1000

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20


    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0


    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Score: {points}', 1, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

    def statistics():
        global dinosaurs, game_speed, ge, population
        text_1 = FONT.render(f'Dinos Alive: {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation: {population.generation}', True, (0, 0, 0))
        text_3 = FONT.render(f'Game Speed: {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_3, (50, 510))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

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
        
        if len(dinosaurs) == 0:
            break

        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                ge[i].fitness = points % 100
                if ge[i].fitness > best_genome_current_gen.fitness:
                    best_genome_current_gen = ge[i]
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 50
                    remove(i)
#        user_input = pygame.key.get_pressed()

        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate((dinosaur.rect.y, distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop), game_speed))
            if output[1] > 0.9 and dinosaur.rect.y == dinosaur.Y_POS:
                dinosaur.big_jump = False 
                dinosaur.dino_jump = True
                dinosaur.dino_run = False
            if output[0] > 0.9 and dinosaur.rect.y == dinosaur.Y_POS:
                dinosaur.big_jump = True
                dinosaur.dino_jump = True
                dinosaur.dino_run = False
 

        statistics()
        score()
        background()
        clock.tick(30)
        pygame.display.update()
    node_names = {0:'Big Jump', 1:'Small Jump',-1: 'Y Position', -2: 'Distance to Obstacle', -3: 'Game Speed'}
    visualize.draw_net(config, best_genome_current_gen, False, node_names=node_names,fmt='jpg')
  

# Setup the NEAT
def run(config_path):
    global population
    # Load configuration.
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path)

    # Create the population, which is the top-level object for a NEAT run.
    checkpoints_list = glob.glob('neat-checkpoint-*')
    if checkpoints_list != []:
        max = checkpoints_list[0]
        for checkpoint in checkpoints_list:
            if checkpoint > max:
                max = checkpoint
        population = neat.Checkpointer.restore_checkpoint(max)
        print(f'using checkpoint {max}')
    else:
        population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.Checkpointer(5, 300))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes,300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    # Visualize the winning genome.



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
