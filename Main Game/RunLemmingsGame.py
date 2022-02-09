# -*- coding: utf-8 -*-
import random
from Platforms import Platforms
from Gates import Gates
from Cursor import Cursor
from Screen import PreGameHUD

''' This is a file to run the whole game, once you run this file you will have
run the whole game with all its classes and functions'''

# ################ CONSTANTS ##########################
# Width and Height of the pyxel
WIDTH = 224
HEIGHT = 256

# Position of platforms (computed randomly)
platPos_x = []
platPos_y = []
platPos_w = []

# First we compute the  length of the platforms from 5 to 10
for i in range(7):
    platPos_w.append(16*random.randint(5, 10))
# Then the x coordenates taking in count that given the length of each platform
# each platform cannot be out of the map
for i in range(7):
    randomx = (random.randint(0, 9)*16)
    while randomx + platPos_w[i] > 211:
        randomx -= 16
    platPos_x.append(randomx)
# Fianlly the y coordenates taking in count there cannot be two platforms in
# the same height
while len(platPos_y) < 7:
    randomx = random.randint(3, 15)
    if randomx*16 not in platPos_y:
        platPos_y.append(randomx*16)
        
# Random number of lemmings from 10 to 20
lemming_number = random.randint(10, 20)

# Variable for the level
level = 1

# Then we give values to the classes required to run the program
platforms = Platforms(platPos_x, platPos_y, platPos_w)
gates = Gates(platforms, platPos_y)
cursor = Cursor()
PreGameHUD(platforms, gates, cursor, WIDTH, HEIGHT)
