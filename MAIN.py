import pygame
from pygame.locals import *

from Gameproperties import Properties
from BlocCazator import Block
from Platforma import Platform


class Game:

    # __init__: This is the constructor of the Game class. It initializes the game platform, a block, and two sprite groups.
    def __init__(self):
        self.PT1 = Platform()
        self.Blocks0 = Block()
        self.all_sprites = pygame.sprite.Group()
        self.blocksgroup = pygame.sprite.Group()

    # loadgrafic: This method initializes the game window, the font, and the clock.
    def loadgrafic(self):
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 16)
        self.FramesPerSec = pygame.time.Clock()
        self.displaysurface = pygame.display.set_mode((Properties.WIDTH, Properties.HEIGHT))
        pygame.display.set_caption('Falling blocks')
        self.bg = pygame.image.load("img/Bg.jpg")

    # reset: This method resets the game by setting the score and speed to 0, and the velocity to 5. It also kills all the entities in the game and adds the platform and a block to the sprite group.
    def reset(self):
        Properties.score = 0
        Properties.speed = 3
        Properties.Vel = 5
        # self.running=False
        for entity in self.all_sprites:
            entity.kill()
        self.PT1.pos = Properties.vec((Properties.WIDTH / 2, Properties.HEIGHT))
        self.PT1.rect.midbottom = self.PT1.pos
        self.all_sprites.add(self.PT1)
        self.createblock()

    # createblock: This method creates a new block and adds it to the sprite group..
    def createblock(self):
        self.Blocks0 = Block()
        self.all_sprites.add(self.Blocks0)
        self.blocksgroup.add(self.Blocks0)

    # update: This method checks if the block has collided with the platform. If it has, it increases the score, speed, and velocity, and creates a new block. If it hasn't, it checks if the block has reached the bottom of the screen. If it has, it prints the score and the maximum score, and resets the game.
    def update(self):
        hits = pygame.sprite.spritecollide(self.PT1, self.blocksgroup, True)
        if hits:
            Properties.score += 1
            Properties.speed += 0.1
            Properties.Vel += 0.1
            self.createblock()
        else:
            if Properties.score > Properties.maxscore:
                Properties.maxscore = Properties.score
            for block in self.blocksgroup:
                if block.rect.y > self.PT1.rect.y:
                    # running = False # Scoate daca vrei sa se termine jocul dupa primul loss
                    print(f"Scorul acestui joc este: {Properties.score}")
                    print(f"Cel mai mare scor de pana acum este: {Properties.maxscore}")
                    self.reset()

    # run: This method runs the game. It loads the graphics, adds the platform and a block to the sprite group, and starts the game loop. The game loop updates the score, moves the platform and the block, and checks for collisions. It also updates the display and sets the frame rate.
    def run(self):
        self.loadgrafic()
        self.blocksgroup.add(self.Blocks0)
        self.all_sprites.add(self.PT1)
        self.all_sprites.add(self.Blocks0)

        while Properties.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    Properties.running = False
            self.displaysurface.fill((255, 255, 255))
            self.displaysurface.blit(self.bg, (0, 0))
            scoretext = self.myfont.render("Score = " + str(Properties.score), 1, (0, 0, 0))
            self.displaysurface.blit(scoretext, (5, 10))
            self.PT1.move()
            for entity in self.all_sprites:
                self.displaysurface.blit(entity.surf, entity.rect)
            for entity in self.blocksgroup:
                entity.moveblock()
                self.update()
            pygame.display.update()
            self.FramesPerSec.tick(Properties.FPS)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

