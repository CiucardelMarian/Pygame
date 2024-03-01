import pygame
from Gameproprieties import Proprieties
import random

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/Licenta.png")
        self.rect = self.surf.get_rect(center=(-100, -100))
        wrandom = random.randint(50, int(Proprieties.WIDTH - 50))
        self.pos = Proprieties.vec((wrandom, 0))

    def moveblock(self):
        self.pos.y += Proprieties.speed
        self.rect.midbottom = self.pos
        if self.pos.y > 800:
            Proprieties.running=False