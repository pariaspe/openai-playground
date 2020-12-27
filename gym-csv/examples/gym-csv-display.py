#!/usr/bin/env python

import gym
import gym_csv
import time

env = gym.make('csv-colored-v0')
env.reset()
env.render()

time.sleep(3)
