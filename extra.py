#!/usr/bin/env python

import gym
import gym_csv

import sys
import os
import numpy as np
import time
from tools import alg_hub

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = LOCAL_PATH + "/{0}.csv"
START = [2,2]
GOAL = [7,7]

# X points down (rows)(v), Y points right (columns)(>), Z would point outwards.
RIGHT = 0  # > Increase Y (column)
UP = 1  # ^ Decrease X (row)
LEFT = 2 # < Decrease Y (column)
DOWN = 3    # v Increase X (row)

SIM_PERIOD_MS = 500.0


def get_command(state, next_state):
    dif = next_state - state
    if dif == 0:
        return 4
    elif dif == 10:
        return RIGHT
    elif dif == -10:
        return LEFT
    elif dif == 1:
        return DOWN
    elif dif == -1:
        return UP
    else:
        return -1


env = gym.make('csv-colored-v0')
state = env.reset()
print("state: " + str(state))
env.render()
time.sleep(0.5)

# Algorithms available: dfs, bfs, dijkstra, astar
route = alg_hub.get_route("map1", START, GOAL, alg="dijkstra")

done = False
while not done:
    try:
        pos = route.pop(0)  # next step
        next_state = pos[0] + pos[1]*10
        command = get_command(state, next_state)
        if command == 4:  # actual pos, continue
            continue
        elif command == -1:
            print("[Error] Bad command.")
            break
    except IndexError:
        command = 0  # no more steps

    state, reward, done, _ = env.step(command)
    env.render()
    print("new_state: " + str(state) + ", reward: " + str(reward) + ", done: " + str(done))
    time.sleep(SIM_PERIOD_MS/1000.0)
