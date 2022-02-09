# -*- coding: utf-8 -*-
import pyxel
from Gates import Gates

''' This file contains the class for the lemmings object.'''


# The lemmings class
class Lemmings:
    def __init__(self, gates: Gates):
        # x and y coordinates.
        self.x = gates.startgate_x
        self.y = gates.startgate_y
        # Velocity in y for exponential free fall.
        self.vy = 0
        # A boolean to express if the lemming is falling at that moment.
        self.fall = False
        # A boolean to represnt the direction of the lemming (left = False).
        self.right = True
        # A boolean to check if the lemming is alive or dead (Dead = False).
        self.alive = True
        # A boolean to check if the lemming has been saved ort not.
        self.saved = False
        # A boolean to express if the lemming has fallen without umbrella.
        self.fell = False
        # A boolean to check if the lemming has an umbrella at the moment.
        self.umbrella = False
        # A boolean to check if the lemming is a blocker.
        self.blocker = False
        # A boolean to check if the lemming is using stairs at the moment.
        self.stairs = False

# A method to update the movements of the lemmings with respect to the borders
# of the map and the platforms.
    def update_lemming(self):
        # Bounce from the map limits
        if self.alive and not self.saved:
            if self.x >= pyxel.width - 12:
                self.right = False
            if self.x <= -4:
                self.right = True

            # Move left and right (note that the velocity when carrying an
            # umbrella and falling is different).
            if not self.umbrella:
                if not self.right and not self.blocker:
                    self.x = self.x - .5
                if self.right and not self.blocker:
                    self.x = self.x + .5
            elif self.umbrella and not self.blocker:
                if self.right:
                    if self.fall:
                        self.x += .5
                    elif not self.fall:
                        self.x += .5
                elif not self.right:
                    if self.fall:
                        self.x -= .1
                    elif not self.fall:
                        self.x -= .5

            # Adding the y velocity to y when free falling.
            self.y += self.vy

            # If falling, velocity in y increases and so does y, otherwise,
            # when the lemming is over a platform, it is 0 (not falling).
            if self.fall:
                if not self.umbrella:
                    self.vy = self.vy + 1
                elif self.umbrella:
                    self.y += .5
            else:
                self.vy = 0

            # If a lemming passes the height limits of the maps (falls to
            # death), it dies.
            if self.y > pyxel.height:
                if self.alive:
                    self.alive = False
