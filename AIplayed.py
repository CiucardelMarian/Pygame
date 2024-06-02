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
        Properties.reward = 0
        # Properties.speed = 3
        # Properties.Vel = 5
        for entity in self.all_sprites:
            entity.kill()
        for entity in self.blocksgroup:
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
            # Properties.speed += 0.1
            # Properties.Vel += 0.1
            self.createblock()
            return 1
        else:
            for block in self.blocksgroup:
                if block.rect.y > self.PT1.rect.y:
                    Properties.running = False
                    return 2
                    # self.reset()
                else:
                    return 3

    def render(self):
        self.displaysurface.fill((255, 255, 255))
        self.displaysurface.blit(self.bg, (0, 0))
        scoretext = self.myfont.render("Score = " + str(Properties.score), 1, (0, 0, 0))
        self.displaysurface.blit(scoretext, (5, 10))
        for entity in self.all_sprites:
            self.displaysurface.blit(entity.surf, entity.rect)
        for entity in self.blocksgroup:
            entity.moveblock()
        pygame.display.update()
        self.FramesPerSec.tick(Properties.FPS)

    def play_step(self, action):
        Properties.reward=0
        oldPosition_x = self.PT1.pos.x
        if action == 0:
            self.PT1.move_left()
            self.actions(oldPosition_x)
        elif action == 1:
            self.PT1.move_right()
            self.actions(oldPosition_x)
        elif action == 2:
            if self.PT1.pos.x - self.Blocks0.pos.x == 0:
                self.PT1.stay_in_place()
        self.render()
        if self.update()==1:
            Properties.reward = 10
        elif self.update()==2:
            Properties.reward -= 2

        return Properties.reward, Properties.running, Properties.score

    def actions(self,oldPositionX):
        if abs(self.PT1.pos.x - self.Blocks0.pos.x) < abs(self.Blocks0.pos.x - oldPositionX):
            Properties.reward = 0.05
        else:
            Properties.reward = -0.1


# def play_step(self, action):
    #     # Properties.reward = 0
    #     oldPosition_x = self.PT1.pos.x
    #     if action == 0:
    #         self.PT1.move_left()
    #         Properties.reward = self.apply_reward_for_left_or_right_move(oldPosition_x, Properties.reward)
    #     elif action == 1:
    #         self.PT1.move_right()
    #         Properties.reward = self.apply_reward_for_left_or_right_move(oldPosition_x, Properties.reward)
    #     elif action == 2:
    #         self.PT1.stay_in_place()
    #         if self.PT1.pos.x - self.Blocks0.pos.x == 0:
    #             Properties.reward += 1
    #         else:
    #             Properties.reward -= 0.1
    #     print("reward: ", Properties.reward)
    #     self.render()
    #     self.update()
    #     return Properties.reward, Properties.running, Properties.score,


 # def apply_reward_for_left_or_right_move(self, oldPosition_x, reward):
    #     if abs(self.PT1.pos.x - self.Blocks0.pos.x) <= abs(self.Blocks0.pos.x - oldPosition_x):
    #         reward += 0.1
    #     else:
    #         reward -= 0.1
    #     # print("reward: ", reward)
    #     return reward
