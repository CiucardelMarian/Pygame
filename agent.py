import torch
import random
import numpy as np
from collections import deque
from training import Linear_QNet, QTrainer
from AIplayed import Game
from plothelper import plot
from Gameproperties import Properties
import pygame

MAX_MEMORY = 1000_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(3, 100, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        # Define the state representation for your game
        # It could be the position of the platform, the position of the falling block, and the velocity of the falling block
        state = [
            game.PT1.pos.x,  # Position of the platform
            game.Blocks0.pos.x,  # Position of the falling block
            Properties.Vel  # Velocity of the falling block
        ]
        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            return
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Define the action selection process for your game
        # It could be moving the platform to the left or right
        # Epsilon-greedy strategy

        if np.random.rand() < self.epsilon:
            # Explore: select a random action
            action = np.random.choice([0, 1])
        else:
            # Exploit: select the action with max value (greedy)
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            action = torch.argmax(prediction).item()
        return action

    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        Properties.maxscore = 0
        game = Game()
        game.loadgrafic()  # Initialize the game window, font, and clock
        game.blocksgroup.add(game.Blocks0)
        game.all_sprites.add(game.PT1)

        while Properties.running:
            # get old state
            state_old = self.get_state(game)

            # get move
            final_move = self.get_action(state_old)

            # perform move and get new state
            reward, done, score = game.play_step(final_move)
            state_new = self.get_state(game)

            # train short memory
            self.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            self.remember(state_old, final_move, reward, state_new, done)

            if done:
                # train long memory, plot result
                game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save()

                print('Game', self.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / self.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

            # Update the display
            game.displaysurface.fill((255, 255, 255))
            game.displaysurface.blit(game.bg, (0, 0))
            scoretext = game.myfont.render("Score = " + str(Properties.score), 1, (0, 0, 0))
            game.displaysurface.blit(scoretext, (5, 10))
            for entity in game.all_sprites:
                game.displaysurface.blit(entity.surf, entity.rect)
            for entity in game.blocksgroup:
                entity.moveblock()

            pygame.display.update()
            game.FramesPerSec.tick(Properties.FPS)

if __name__ == "__main__":

    agent = Agent()
    agent.train()