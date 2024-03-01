import pygame
from Gameproperties import Properties
import random

class Block(pygame.sprite.Sprite):

    # __init__: This is the constructor of the Block class. It initializes the block's surface, rectangle, and position.
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/Licenta.png")
        self.rect = self.surf.get_rect(center=(-100, -100))
        wrandom = random.randint(50, int(Properties.WIDTH - 50))
        self.pos = Properties.vec((wrandom, 0))

    # moveblock: This method moves the block down the screen. If the block reaches the bottom of the screen, it sets the running variable to False.
    def moveblock(self):
        self.pos.y += Properties.speed
        self.rect.midbottom = self.pos
        if self.pos.y > 800:
            Properties.running=False