import pygame
from pygame.locals import *
import random
# Initialisation
pygame.init()
vec = pygame.math.Vector2  # 2 for two-dimensional
HEIGHT = 800
WIDTH = 1000
Vel = 5
i = 0
j = 1
FPS = 120
FramesPerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Falling blocks')

# GameObjects


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, 70))
        self.surf.fill((96, 152, 247))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT))

        self.pos = vec((WIDTH / 2, HEIGHT))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.pos.x -= Vel
        if pressed_keys[K_RIGHT]:
            self.pos.x += Vel

        if self.pos.x > WIDTH - 50:
            self.pos.x = WIDTH - 50
        if self.pos.x < 50:
            self.pos.x = 50

        self.rect.midbottom = self.pos


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, 100))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center=(-100, -100))
        wrandom = random.randint(50, int(WIDTH - 50))
        self.pos = vec((wrandom, 0))

    def moveblock(self):
        self.pos.y += 3
        self.rect.midbottom = self.pos

    def update(self):
        global j
        hits = pygame.sprite.spritecollide(self, all_sprites, False)
        if len(hits) > j:
            j += 1
            createblock()
        for hit in hits:
            if hit == PT1:  # Check if the collided sprite is PT1 (Platform)
                self.pos.y = hit.rect.top + 1
                self.rect.midbottom = self.pos
                self.pos.x = PT1.pos.x
                self.rect.midbottom = self.pos


def createblock():
    global i
    i += 1
    globals()['Blocks'+str(i)] = Block()
    all_sprites.add(globals()['Blocks'+str(i)])
    blocksgroup.add(globals()['Blocks' + str(i)])




PT1 = Platform()
Blocks0 = Block()
all_sprites = pygame.sprite.Group()
blocksgroup = pygame.sprite.Group()
blocksgroup.add(Blocks0)
all_sprites.add(PT1)
all_sprites.add(Blocks0)

running = True
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    displaysurface.fill((255, 255, 255))
    PT1.move()
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    for entity in blocksgroup:
        entity.moveblock()
        entity.update()
    pygame.display.update()
    FramesPerSec.tick(FPS)
