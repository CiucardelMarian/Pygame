import pygame
from pygame.locals import *
from Gameproperties import Properties


class Platform(pygame.sprite.Sprite):

    # __init__: This is the constructor of the Platform class. It initializes the platform's surface, rectangle, and position.
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/BodoRemastered.png")
        self.rect = self.surf.get_rect(center=(Properties.WIDTH/2, Properties.HEIGHT))
        self.pos = Properties.vec((Properties.WIDTH / 2, Properties.HEIGHT))

    # move: This method moves the platform left or right based on the keys pressed. It also sets the platform's position to the middle of the screen if it goes out of bounds.
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.pos.x -= Properties.Vel
        if pressed_keys[K_RIGHT]:
            self.pos.x += Properties.Vel

        if self.pos.x > Properties.WIDTH - 100:
            self.pos.x = Properties.WIDTH - 100
        if self.pos.x < 100:
            self.pos.x = 100
        self.rect.midbottom = self.pos

    def move_left(self):
        self.pos.x -= Properties.Vel
        if self.pos.x < 100:
            self.pos.x = 100
        self.rect.midbottom = self.pos

    def move_right(self):
        self.pos.x += Properties.Vel
        if self.pos.x > Properties.WIDTH - 100:
            self.pos.x = Properties.WIDTH - 100
        self.rect.midbottom = self.pos

    def stay_in_place(self):
        self.rect.midbottom = self.pos
