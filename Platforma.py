import pygame
from pygame.locals import *
from Gameproprieties import Proprieties

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/BodoRemastered.png")
        self.rect = self.surf.get_rect(center=(Proprieties.WIDTH/2, Proprieties.HEIGHT))
        self.pos = Proprieties.vec((Proprieties.WIDTH / 2, Proprieties.HEIGHT))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.pos.x -= Proprieties.Vel
        if pressed_keys[K_RIGHT]:
            self.pos.x += Proprieties.Vel

        if self.pos.x > Proprieties.WIDTH - 100:
            self.pos.x = Proprieties.WIDTH - 100
        if self.pos.x < 100:
            self.pos.x = 100

        self.rect.midbottom = self.pos
