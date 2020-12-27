#!/usr/bin/env python

import gym
import gym_csv

import numpy as np
import time

# X points down (rows)(v), Y points right (columns)(>), Z would point outwards.
RIGHT = 0  # > Increase Y (column)
UP = 1  # ^ Decrease X (row)
LEFT = 2 # < Decrease Y (column)
DOWN = 3    # v Increase X (row)

SIM_PERIOD_MS = 500.0

env = gym.make('csv-pygame-v0')
state = env.reset()
print("state: " + str(state))
env.render()
time.sleep(0.5)

for i in range(5):
    new_state, reward, done, _ = env.step(RIGHT)
    env.render()
    print("new_state: " + str(new_state) + ", reward: " + str(reward) + ", done: " + str(done))
    time.sleep(SIM_PERIOD_MS/1000.0)


for i in range(6):
    new_state, reward, done, _ = env.step(DOWN)
    env.render()
    print("new_state: " + str(new_state) + ", reward: " + str(reward) + ", done: " + str(done))
    time.sleep(SIM_PERIOD_MS/1000.0)
