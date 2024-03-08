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
        self.update()
        self.render()

    def update(self):

        hits = pygame.sprite.spritecollide(self.PT1, self.blocksgroup, True)
        if hits:
            Properties.score += 1
            Properties.speed += 0.1
            Properties.Vel += 0.1
            self.createblock()
            return True
        else:
            if Properties.score > Properties.maxscore:
                Properties.maxscore = Properties.score
            for block in self.blocksgroup:
                if block.rect.y > self.PT1.rect.y:
                    # Properties.running = False
                    return False
                    self.reset()
                else:
                    pass

    def render(self):
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

    def play_step(self, action):
        if action == 0:
            self.PT1.move_left()
        elif action == 1:
            self.PT1.move_right()
        reward=0
        self.render()
        if self.update():
            reward = 1
        else:
            reward = -1

        return reward, Properties.running, Properties.score
