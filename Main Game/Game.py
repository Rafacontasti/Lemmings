# -*- coding: utf-8 -*-
import pyxel
import random
from Platforms import Platforms
from Lemming import Lemmings
from Gates import Gates
from Cursor import Cursor
from Tools import Umbrella, BlockerSign, Stairs

'''This is the file containing the main logic of the whole game. it is
automatically run by the initial screen class. It contains all the classes
and objects used in the development of our game.'''

# ############### CONSTANTS #################
WIDTH = 224
HEIGHT = 256
lemming_number = random.randint(10, 20)
level = 1


# ############## MAIN CLASS ################
class Game:
    def __init__(self, platforms: Platforms, gates: Gates, cursor: Cursor):
        # Initiating the pyxel module and loading the pyxres file.
        pyxel.init(WIDTH, HEIGHT, caption="Lemmings Game")
        pyxel.load("sprites.pyxres")

        # Main lemming obects list.
        self.lemmings = []
        # Gates object to import the positions of the gates.
        self.gates = gates
        # Cursor object to import the positions of the cursor.
        self.cursor = cursor
        # Main list for the umbrellas objects.
        self.umbrellas = []
        # Main list of the platforms
        self.platform = platforms.platforms
        # Lists to count and keep record of which lemmings dies, is a blocker,
        # is saved and a list for the stairs.
        self.alive = []
        self.blockers = []
        self.stairs = []
        self.saved = []
        # Command to play the music in a loop.
        pyxel.playm(0, loop=True)
        # Running the pyxel module.
        pyxel.run(self.update, self.draw)

# Update method executed every frame.
    def update(self):
        # If the Q key is pressed, the program ends.
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # A lemming is created every 25 frames and added to the list.
        if pyxel.frame_count % 25 == 0 and len(self.lemmings) < lemming_number:
            self.lemmings.append(Lemmings(self.gates))
            self.alive.append(True)
            self.saved.append(False)

        # Keeps the dead lemmings list updated
        for i in range(len(self.lemmings)):
            if not self.lemmings[i].alive:
                self.alive[i] = False
        # Invoke the update_lemming method for every lemming in the list.
        for lemming in self.lemmings:
            lemming.update_lemming()
        # Invoking the update_platform method
        for i, v in enumerate(self.platform):
            self.platform[i] = self.update_platform(*v)

        # Updating the position of the cursor when arrow keys are pressed.
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.cursor.x < pyxel.width - 16:
            self.cursor.x += 16
        if pyxel.btnp(pyxel.KEY_LEFT) and self.cursor.x > 0:
            self.cursor.x -= 16
        if pyxel.btnp(pyxel.KEY_UP) and self.cursor.y > 0:
            self.cursor.y -= 16
        if pyxel.btnp(pyxel.KEY_DOWN) and self.cursor.y < pyxel.height - 16:
            self.cursor.y += 16

        # If the W key is pressed, a new umbrella is added to the list at the
        # position of the cursor.
        if pyxel.btnp(pyxel.KEY_W):
            self.umbrellas.append(Umbrella(self.cursor))
        # If the E key is pressed, a new blocker sign is added to the list at
        # the position of the cursor.
        if pyxel.btnp(pyxel.KEY_E):
            self.blockers.append(BlockerSign(self.cursor))
        # If the A key is pressed, a left faced ladder is added to the list at
        # the position of the cursor.
        if pyxel.btnp(pyxel.KEY_A):
            self.stairs.append(Stairs(self.cursor, False, self.lemmings))
        # If the S key is pressed, a right faced ladder is added to the list at
        # the position of the cursor.
        if pyxel.btnp(pyxel.KEY_S):
            self.stairs.append(Stairs(self.cursor, True, self.lemmings))

        # If a lemming reaches an umbrella, it grabs it and the umbrella is
        # removed from the list.
        for umbrella in self.umbrellas:
            for lemming in self.lemmings:
                if (lemming.y == umbrella.y and lemming.x == umbrella.x
                        and not lemming.umbrella):
                    lemming.umbrella = True
                    self.umbrellas.remove(umbrella)
        # If a lemming reaches a blocker sign, it becomes a blocker and the
        # sign is removed from the list. A platform is added at the lemming
        # position to reduce code.
        for blockersign in self.blockers:
            for lemming in self.lemmings:
                if (lemming.x <= blockersign.x + 2
                        and lemming.y == blockersign.y
                        and lemming.x >= blockersign.x - 2):
                    lemming.blocker = True
                    self.blockers.remove(blockersign)
                    self.platform.append([lemming.x, lemming.y, 16, False])
        # If a lemming reaches a ladder, it will climb it if it goes the same
        # direction than the ladder, else it will descend it.
        for stair in self.stairs:
            for lemming in self.lemmings:
                if stair.right and lemming.right:
                    if (lemming.x + 12 >= stair.x and lemming.y >= stair.y - 16
                            and lemming.x < stair.x + 16):
                        lemming.y -= .5
                        lemming.stairs = True
                        lemming.fall = False
                    else:
                        lemming.stairs = False
                elif stair.right and not lemming.right:
                    if (lemming.x <= stair.x + 16 and lemming.y < stair.y
                            and lemming.x):
                        lemming.y += .5
                        lemming.stairs = True
                        lemming.fall = False
                    else:
                        lemming.stairs = False
                elif not stair.right and not lemming.right:
                    if lemming.x <= stair.x + 12 and lemming.y > stair.y - 16:
                        lemming.y -= .5
                        lemming.stairs = True
                        lemming.fall = False
                    else:
                        lemming.stairs = False
                elif not stair.right and lemming.right:
                    if lemming.x + 4 >= stair.x and lemming.y < stair.y:
                        lemming.y += .5
                        lemming.stairs = True
                        lemming.fall = False
                    else:
                        lemming.stairs = False

        # If a lemming reaches the final door, it is saved
        for lemming in self.lemmings:
            if (lemming.x <= self.gates.endgate_x + 10
                    and lemming.x >= self.gates.endgate_x - 10
                    and lemming.y >= self.gates.endgate_y - 5
                    and lemming.y <= self.gates.endgate_y + 5):
                lemming.saved = True
                self.saved[self.lemmings.index(lemming)] = True

    # A method to update the fall and changes of direction for the lemmings
    # when colliding with the platforms.
    def update_platform(self, x, y, length, is_pl):
        # Method is applied to every lemming.
        for lemming in self.lemmings:
            # If lemming is right above the platform, it will not fall.
            if (lemming.x + 16 >= x
                    and lemming.x <= x + length
                    and lemming.y + 16 >= y
                    and lemming.y + 16 <= y + 16):
                lemming.vy = 0
                lemming.fall = False

                # If the lemming has fallen without umbrella it wil die.
                if (lemming.fell and pyxel.frame_count > 20
                        and not lemming.umbrella and not lemming.stairs):
                    lemming.alive = False
                    self.alive[self.lemmings.index(lemming)] = False

            # If the lemming does not have a platform below, it falls.
            elif (lemming.y + 16 >= y and lemming.y + 16 <= y + 16
                    and not lemming.stairs):
                if lemming.x + 16 < x or lemming.x > x + length:
                    lemming.fall = True

            # If the lemming hits a platform from the right, it changes
            # directtion.
            if (lemming.y + 16 >= y and lemming.y <= y + 16
                    and lemming.x + 12 == x):
                lemming.right = False
            # If the lemming hits a platform from the left, it changes
            # directtion.
            if (lemming.y + 16 >= y and lemming.y <= y + 16
                    and lemming.x == x + (length-6)):
                lemming.right = True
            # If the lemming is below the gate, it has already fallen.
            if lemming.y > self.gates.startgate_y:
                lemming.fell = True

        return x, y, length, is_pl

# Draw method to draw everything on the pyxel screen.
    def draw(self):
        # Background color (Black = 0).
        pyxel.cls(0)

        # Scoreboard values on top of the screen.
        pyxel.text(3, 3, "Level: %i" % (level), 7)
        pyxel.text(59, 3, "Alive: %i" % (self.alive.count(True)), 7)
        pyxel.text(115, 3, "Saved: %i" % (self.saved.count(True)), 7)
        pyxel.text(171, 3, "Died: %i" % (self.alive.count(False)), 7)
        pyxel.text(3, 15, "Ladders: %i" % (len(self.stairs)), 7)
        pyxel.text(77, 15, "Umbrellas: %i" % (len(self.umbrellas)), 7)
        pyxel.text(151, 15, "Blockers: %i" % (len(self.platform)-7), 7)

        # Draw all the platforms.
        for x, y, length, is_pl in self.platform:
            if is_pl:
                for j in range(x, x+length, 16):
                    pyxel.blt(j, y, 0, 32, 0, 16, 16, colkey=0)

        # Draw the start and end doors.
        pyxel.blt(self.gates.startgate_x, self.gates.startgate_y, 0, 0, 16, 16,
                  16, colkey=0)
        pyxel.blt(self.gates.endgate_x, self.gates.endgate_y, 0, 16, 16, 16,
                  16, colkey=0)

        # Animation constant that changes with the frames
        animate = 0
        if pyxel.frame_count % 19 >= 0 and pyxel.frame_count % 19 < 5:
            animate = 0
        elif pyxel.frame_count % 19 >= 5 and pyxel.frame_count % 19 < 10:
            animate = 1
        elif pyxel.frame_count % 19 >= 10 and pyxel.frame_count % 19 < 15:
            animate = 2
        elif pyxel.frame_count % 19 >= 15 and pyxel.frame_count % 19 < 20:
            animate = 3

        # Draw the lemmings
        for lemming in self.lemmings:
            if lemming.alive and not lemming.saved:
                if not lemming.umbrella and not lemming.blocker:
                    # Sprites for right direction.
                    if lemming.right:
                        pyxel.blt(lemming.x, lemming.y, 1, animate * 16, 0, 16,
                                  16, colkey=0)
                    # Sprites for left direction.
                    elif not lemming.right:
                        pyxel.blt(lemming.x, lemming.y, 1, animate * 16, 16,
                                  16, 16, colkey=0)

                # Sprites for lemming with umbrella.
                elif lemming.umbrella and not lemming.blocker:
                    if lemming.right:
                        pyxel.blt(lemming.x, lemming.y, 1, animate * 16, 64,
                                  16, 16, colkey=0)
                    elif not lemming.right:
                        pyxel.blt(lemming.x, lemming.y, 1, animate * 16, 96,
                                  16, 16, colkey=0)

                # Sprites for blocker lemming
                elif lemming.blocker:
                    pyxel.blt(lemming.x, lemming.y, 1, animate * 16, 48, 16,
                              16, colkey=0)

            # Sprites for dead lemming
            elif not lemming.alive and not lemming.saved:
                self.animateDeath = 0
                if self.animateDeath < 5:
                    if pyxel.frame_count % 20 == 0:
                        self.animateDeath += 1
                    pyxel.blt(lemming.x, lemming.y, 1, animate * 16, 80, 16,
                              16, colkey=0)
        pyxel.blt(self.cursor.x, self.cursor.y, 2,
                  16 if pyxel.frame_count % 30 < 15 else 0, 48, 16, 16,
                  colkey=0)

        # Draw umbrellas
        for u in self.umbrellas:
            pyxel.blt(u.x, u.y, 2, 16 * animate, 16, 16, 16, colkey=0)

        # Draw blockers
        for b in self.blockers:
            pyxel.blt(b.x, b.y, 0, 0, 48, 16, 16, colkey=0)

        # Draw stairs
        for s in self.stairs:
            # Right directioned
            if s.right:
                pyxel.blt(s.x, s.y, 2, 16, 0, 16, 16, colkey=0)
            # Left directioned
            if not s.right:
                pyxel.blt(s.x, s.y, 2, 0, 0, 16, 16, colkey=0)
