# -*- coding: utf-8 -*-

import pyxel
import random
from Platforms import Platforms
from Lemming import Lemmings
from Gates import Gates
from Cursor import Cursor
from Tools import Umbrella, BlockerSign, Stairs
from Game import Game
from Screen import PreGameHUD



# Here we declare the initial variables
WIDTH = 224
HEIGHT = 256
platPos_x = []
platPos_y = []
platPos_w = []
lemming_number = random.randint(10, 20)
level = 1

for w in range(7):
    platPos_w.append(16*random.randint(5, 10))

for w in range(7):
    randomx = (random.randint(0, 9)*16)
    while randomx + platPos_w[w] > 211:
        randomx -= 16
    platPos_x.append(randomx)

while len(platPos_y) < 7:
    randomx = random.randint(3, 15)
    if randomx*16 not in platPos_y:
        platPos_y.append(randomx*16)



platforms = Platforms(platPos_x, platPos_y, platPos_w)
gates = Gates(platforms, platPos_y)
cursor = Cursor()
PreGameHUD(platforms, gates, cursor)
