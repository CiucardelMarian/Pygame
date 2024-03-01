import pygame
from pygame.locals import *

from Gameproprieties import Proprieties
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
        self.displaysurface = pygame.display.set_mode((Proprieties.WIDTH, Proprieties.HEIGHT))
        pygame.display.set_caption('Falling blocks')
        self.bg = pygame.image.load("img/Bg.jpg")

    def reset(self):
        Proprieties.score = 0
        Proprieties.speed = 3
        Proprieties.Vel = 5
        # self.running=False
        for entity in self.all_sprites:
            entity.kill()
        self.PT1.pos = Proprieties.vec((Proprieties.WIDTH / 2, Proprieties.HEIGHT))
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
            Proprieties.score += 1
            Proprieties.speed += 0.1
            Proprieties.Vel += 0.1
            self.createblock()
        else:
            if Proprieties.score > Proprieties.maxscore:
                Proprieties.maxscore = Proprieties.score
            for block in self.blocksgroup:
                if block.rect.y > self.PT1.rect.y:
                    # running = False # Scoate daca vrei sa se termine jocul dupa primul loss
                    print(f"Scorul acestui joc este: {Proprieties.score}")
                    print(f"Cel mai mare scor de pana acum este: {Proprieties.maxscore}")
                    self.reset()

    def run(self):
        self.loadgrafic()
        self.blocksgroup.add(self.Blocks0)
        self.all_sprites.add(self.PT1)
        self.all_sprites.add(self.Blocks0)

        while Proprieties.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    Proprieties.running = False
            self.displaysurface.fill((255, 255, 255))
            self.displaysurface.blit(self.bg, (0, 0))
            scoretext = self.myfont.render("Score = " + str(Proprieties.score), 1, (0, 0, 0))
            self.displaysurface.blit(scoretext, (5, 10))
            self.PT1.move()
            for entity in self.all_sprites:
                self.displaysurface.blit(entity.surf, entity.rect)
            for entity in self.blocksgroup:
                entity.moveblock()
                self.update()
            pygame.display.update()
            self.FramesPerSec.tick(Proprieties.FPS)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

