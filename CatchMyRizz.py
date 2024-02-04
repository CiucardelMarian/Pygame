import pygame
from pygame.locals import *
import random
import sys
# Initialisation
pygame.init()
vec = pygame.math.Vector2  # 2 for two-dimensional
HEIGHT = 800
WIDTH = 1000
Vel = 5
speed = 3
score = 0
myfont = pygame.font.SysFont("monospace", 16)
FPS = 120
FramesPerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Falling blocks')

# GameObjects


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/iqos.png")
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


def update():
    global score, speed, Vel
    hits = pygame.sprite.spritecollide(PT1, blocksgroup, True)
    for hit in hits:
        score += 1
        speed += 0.1
        Vel += 0.1
        createblock()

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/Pachet.png")
        self.rect = self.surf.get_rect(center=(-100, -100))
        wrandom = random.randint(50, int(WIDTH - 50))
        self.pos = vec((wrandom, 0))

    def moveblock(self):
        self.pos.y += speed
        self.rect.midbottom = self.pos
        if self.pos.y > 800:
            pygame.quit()


def createblock():
    Blocks0 = Block()
    all_sprites.add(Blocks0 )
    blocksgroup.add(Blocks0)




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
    scoretext = myfont.render("Score = " + str(score), 1, (0, 0, 0))
    displaysurface.blit(scoretext, (5, 10))
    print(score)
    PT1.move()
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    for entity in blocksgroup:
        entity.moveblock()
        entity.update()
    update()
    pygame.display.update()
    FramesPerSec.tick(FPS)
