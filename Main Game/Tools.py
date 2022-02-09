# -*- coding: utf-8 -*-
from Cursor import Cursor

''' This file contains the tools (or functionalities of lemmings) of the game,
these are the umbrella, the stairs (ladder) and the blocker lemming.'''


# A class for the Umbrella object.
class Umbrella:
    def __init__(self, cursor: Cursor):
        # x and y coordinates
        self.x = cursor.x
        self.y = cursor.y


# A class for the Stairs object.
class Stairs:
    def __init__(self, cursor: Cursor, right: bool, lemmingslist: list):
        # x and y coordinates.
        self.x = cursor.x
        self.y = cursor.y
        # Direction of ladder.
        self.right = right
        # Input for the main list with the lemmings to work more confortable
        # when moving the lemmings through the ladder.
        self.lemmingslist = lemmingslist


# A class for the blocker object.
class BlockerSign:
    def __init__(self, cursor: Cursor):
        # x and y coordinates.
        self.x = cursor.x
        self.y = cursor.y
