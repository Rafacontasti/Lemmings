# -*- coding: utf-8 -*-
import random
from Platforms import Platforms

''' This file contains the object for the gates'''


# A class for the entrance and objective door.
class Gates:

    def __init__(self, platforms: Platforms, platPos_y):
        # Random variables that use the lists of the platforms to place the
        # doors at random positions of the platforms of that specific game.
        random1 = random.randint(0, 6)
        random2 = random.randint(5, ((platforms.platforms[random1][2])/16))
        random1_1 = random.randint(0, 6)
        random2_2 = random.randint(5, ((platforms.platforms[random1][2])/16))

        # Assign the x and y positions for the gates randomly.
        self.startgate_x = (platforms.platforms[random1][0]) + ((random2-5)*16)
        self.startgate_y = (platforms.platforms[random1][1]) - 16
        # We set the end gate first equal to the start gate and then use a
        # while loop to make sure they are not at the same platform and place.
        self.endgate_x = self.startgate_x
        self.endgate_y = self.startgate_y
        while self.endgate_y == self.startgate_y:
            self.endgate_x = int((platforms.platforms[random1_1][0]) +
                                 ((random2_2-5)*16))
            self.endgate_y = int((platforms.platforms[random1_1][1]) - 16)
