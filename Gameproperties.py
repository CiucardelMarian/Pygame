# This file contains the game proprieties and the game settings
import pygame

class Properties():

    # __init__: This is the constructor of the Properties class. It initializes the game properties.
    vec = pygame.math.Vector2
    HEIGHT = 800
    WIDTH = 1000
    Vel = 7 # la ce viteza se deplaseaza platforma
    speed = 5 # la ce viteza cade blocul
    score = 0
    maxscore = 0
    FPS = 60
    running = True
    n_games = 0
    reward=0