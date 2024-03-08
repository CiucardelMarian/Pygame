import torch
import random
import numpy as np
from collections import deque
from training import Linear_QNet, QTrainer
from MAIN import Game
from plothelper import plot
from Gameproperties import Properties
import pygame

MAX_MEMORY = 1000_000
BATCH_SIZE = 1000
LR = 0.01

class Agent:

    def __init__(self):
        Properties.n_games = 0
        self.epsilon = 100 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(3, 256, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        # Define the state representation for your game
        state = np.array([
            game.PT1.pos.x,  # Position of the platform
            game.Blocks0.pos.x,  # Position of the falling block
            Properties.Vel  # Velocity of the falling block
        ],dtype=float)
        return state

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
        self.epsilon = max(100 - Properties.n_games, 50)
        if random.randint(0, 200) < self.epsilon:
            # Explore: select a random action
            final_move = np.random.choice([0, 1])
        else:
            # Exploit: select the action with max value (greedy)
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()
        return final_move

    def train(self):
        game = Game()
        game.loadgrafic()
        game.blocksgroup.add(game.Blocks0)
        game.all_sprites.add(game.PT1)

        while Properties.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Properties.running = False
            if not Properties.running:
                break
            state_old = self.get_state(game)
            final_move = self.get_action(state_old)
            reward, done, score = game.play_step(final_move)
            state_new = self.get_state(game)
            self.train_short_memory(state_old, final_move, reward, state_new, done)
            self.remember(state_old, final_move, reward, state_new, done)

            if Properties.running == False:
                game.reset()
                Properties.n_games += 1
                self.train_long_memory()

                if Properties.score > Properties.maxscore:
                    Properties.maxscore = Properties.score
                    self.model.save()

                print('Game', Properties.n_games, 'Score', score, 'Record:', Properties.maxscore)

if __name__ == "__main__":

    agent = Agent()
    agent.train()