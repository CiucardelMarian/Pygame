import pygame
from pygame.locals import *

from Gameproperties import Properties
from BlocCazator import Block
from Platforma import Platform


class Game:

    def __init__(self):
        self.PT1 = Platform()
        self.Blocks0 = Block()
        self.all_sprites = pygame.sprite.Group()
        self.blocksgroup = pygame.sprite.Group()

    def loadgrafic(self):
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 16)
        self.FramesPerSec = pygame.time.Clock()
        self.displaysurface = pygame.display.set_mode((Properties.WIDTH, Properties.HEIGHT))
        pygame.display.set_caption('Falling blocks')
        self.bg = pygame.image.load("img/Bg.jpg")

    def reset(self):
        Properties.score = 0
        Properties.speed = 3
        Properties.Vel = 5
        for entity in self.all_sprites:
            entity.kill()
        self.PT1.pos = Properties.vec((Properties.WIDTH / 2, Properties.HEIGHT))
        self.PT1.rect.midbottom = self.PT1.pos
        self.all_sprites.add(self.PT1)
        self.createblock()

    def createblock(self):
        self.Blocks0 = Block()
        self.all_sprites.add(self.Blocks0)
        self.blocksgroup.add(self.Blocks0)

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
                    running = False
                    print(f"Scorul acestui joc este: {Properties.score}")
                    print(f"Cel mai mare scor de pana acum este: {Properties.maxscore}")
                    self.reset()

    def play_step(self, action):
        if action == 0:
            self.PT1.move_left()
        elif action == 1:
            self.PT1.move_right()
        self.update()

        reward = 0
        hits = pygame.sprite.spritecollide(self.PT1, self.blocksgroup, True)
        if hits:
            reward = 1
            self.createblock()
        elif self.Blocks0.pos.y > 800:
            reward = -1
            self.reset()

        done = not Properties.running
        score = Properties.score

        return reward, done, score

    def run(self):
        self.loadgrafic()
        self.blocksgroup.add(self.Blocks0)
        self.all_sprites.add(self.PT1)

        while Properties.running:
            self.displaysurface.fill((255, 255, 255))
            self.displaysurface.blit(self.bg, (0, 0))
            scoretext = self.myfont.render("Score = " + str(Properties.score), 1, (0, 0, 0))
            self.displaysurface.blit(scoretext, (5, 10))

            for entity in self.all_sprites:
                self.displaysurface.blit(entity.surf, entity.rect)
            for entity in self.blocksgroup:
                entity.moveblock()

            self.update()

            pygame.display.update()
            self.FramesPerSec.tick(Properties.FPS)

        pygame.quit()

