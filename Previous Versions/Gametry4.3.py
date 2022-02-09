# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:55:10 2020

@author: Rafael Contasti

Game try 2.0
"""

import pyxel
import random
from Platforms import Platforms

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
# The platforms class
class Platforms:
    def __init__(self, platPos_x, platPos_y, platPos_w):
        self.platforms = []

        for n in range(len(platPos_x)):
            self.platforms.append([platPos_x[n],
                                   platPos_y[n],
                                   platPos_w[n],
                                   True])
    
    @property
    def platforms(self):
        return self.__platforms

    @platforms.setter
    def platforms(self, platPos_x: list):
        for x in platPos_x:
            if x < 0:
                platPos_x[x] = 0

        for y in platPos_y:
            if y < 0:
                platPos_y[y] = 0

        for x in platPos_x:
            if x < 0:
                platPos_x[i] = 0
        for n in range(len(platPos_x)):
            self.__platforms.append([platPos_x[n],
                                   platPos_y[n],
                                   platPos_w[n],
                                   True])
        
# The class for the doors
class Gates:
    def __init__(self, platforms: Platforms, platPos_y):
        
        random1 = random.randint(0, 6)
        random2 = random.randint(5, ((platforms.platforms[random1][2])/16))
        random1_1 = random.randint(0, 6)
        random2_2 = random.randint(5, ((platforms.platforms[random1][2])/16))

        self.startgate_x = (platforms.platforms[random1][0]) + ((random2-5)*16)
        self.startgate_y = (platforms.platforms[random1][1]) - 16
        self.endgate_x = self.startgate_x
        self.endgate_y = self.startgate_y
        while self.endgate_y == self.startgate_y:
            self.endgate_x = int((platforms.platforms[random1_1][0]) + ((random2_2-5)*16))
            self.endgate_y = int((platforms.platforms[random1_1][1]) - 16)

        

# The lemmings class
class Lemmings:
    def __init__(self, gates: Gates):
        self.x = gates.startgate_x
        self.y = gates.startgate_y
        self.vy = 0
        self.fall = False
        self.right = True
        self.alive = True
        self.saved = False
        self.fell = False
        self.umbrella = False
        self.blocker = False
        self.stairs = False
    
    @property
    def vy(self):
        return self.__vy

    @vy.setter
    def vy(self, vy: int):
        if vy >= 0:
            self.__v = age
        else:
            self.__age = 0

# A method to update the movements of the lemmings
    def update_lemming(self):
        if self.alive and not self.saved:
            if self.x >= pyxel.width - 12:
                self.right = False
            if self.x <= -4:
                self.right = True

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
        
            self.y += self.vy
        
            if self.fall:
                if not self.umbrella:
                    self.vy = self.vy + 1
                elif self.umbrella:
                    self.y += .5
            else:
                self.vy = 0
        
            if self.y > pyxel.height:
                if self.alive:
                    self.alive = False
            
        



class Cursor:
    def __init__(self):
        self.x = 112
        self.y = 144
    

class PreGameHUD:
    def __init__(self,):
        pyxel.init(WIDTH, HEIGHT, caption="Lemmings Game")
        pyxel.image(0).load(0, 0, "assets/lemmingsTitle.png")

        pyxel.run(self.update, self.draw)
    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            Game(plat, gat, curs)
            pyxel.quit()
    def draw(self):
        pyxel.cls(0)
        pyxel.blt(16, 96, 0, 0, 0, 192, 64)
        colortext = pyxel.frame_count % 25
        pyxel.text(69, 151, "Press ENTER to start", 7 if colortext < 10 else 0)
        pyxel.text(0, pyxel.height - 16, "          By Rafael Contasti and Carlos Iborra", 7)

class Umbrella:
    def __init__(self, cursor: Cursor):
        self.x = cursor.x
        self.y = cursor.y

class BlockerSign:
    def __init__(self, cursor: Cursor, sign: bool = True, lemming: Lemmings = None):
        self.sign = sign
        if sign:
            self.x = cursor.x
            self.y = cursor.y
        else:
            self.x = lemming.x
            self.y = lemming.y

class Stairs:
    def __init__(self, cursor: Cursor, right: bool, lemmingslist: list):
        self.x = cursor.x
        self.y = cursor.y
        self.right = right
        self.lemmingslist = lemmingslist


class Game:
    def __init__(self, platforms: Platforms, gates: Gates, cursor: Cursor):
        pyxel.init(WIDTH, HEIGHT, caption="Lemmings Game")

        pyxel.load("sprites.pyxres")

        self.lemmings = []
        self.gates = gates
        self.cursor = cursor
        self.umbrellas = []
        self.alive = []
        self.blockers = []
        self.stairs = []
        self.saved = []

        self.platform = platforms.platforms
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
        if pyxel.frame_count % 25 == 0 and len(self.lemmings) < lemming_number:
            self.lemmings.append(Lemmings(self.gates))
            self.alive.append(True)
            self.saved.append(False)

        for i in range(len(self.lemmings)):
            if not self.lemmings[i].alive:
                self.alive[i] = False
        
        for lemming in self.lemmings:
            lemming.update_lemming()

        for i, v in enumerate(self.platform):
            self.platform[i] = self.update_platform(*v)

        if pyxel.btnp(pyxel.KEY_RIGHT) and self.cursor.x < pyxel.width - 16:
            self.cursor.x += 16
        if pyxel.btnp(pyxel.KEY_LEFT) and self.cursor.x > 0:
            self.cursor.x -= 16
        if pyxel.btnp(pyxel.KEY_UP) and self.cursor.y > 0:
            self.cursor.y -= 16
        if pyxel.btnp(pyxel.KEY_DOWN) and self.cursor.y < pyxel.height - 16:
            self.cursor.y += 16

        if pyxel.btnp(pyxel.KEY_W):
            self.umbrellas.append(Umbrella(self.cursor))
        if pyxel.btnp(pyxel.KEY_E):
            self.blockers.append(BlockerSign(self.cursor))
        if pyxel.btnp(pyxel.KEY_A):
            self.stairs.append(Stairs(self.cursor, False, self.lemmings))
        if pyxel.btnp(pyxel.KEY_S):
            self.stairs.append(Stairs(self.cursor, True, self.lemmings))
        
        for umbrella in self.umbrellas:
            for lemming in self.lemmings:
                if lemming.y == umbrella.y and lemming.x == umbrella.x and not lemming.umbrella:
                    lemming.umbrella = True
                    self.umbrellas.remove(umbrella)
        for blockersign in self.blockers:
            for lemming in self.lemmings:
                if lemming.x <= blockersign.x + 2 and lemming.y == blockersign.y and lemming.x >= blockersign.x - 2:
                    lemming.blocker = True
                    self.blockers.remove(blockersign)
                    self.platform.append([lemming.x, lemming.y, 16, False])
        for stair in self.stairs:
            for lemming in self.lemmings:
                if stair.right and lemming.right:
                    if lemming.x + 12 >= stair.x and lemming.y >= stair.y - 16 and lemming.x < stair.x + 16:
                        lemming.y -= .5
                        lemming.stairs = True
                        lemming.fall = False
                    else:
                        lemming.stairs = False
                elif stair.right and not lemming.right:
                    if lemming.x <= stair.x + 16 and lemming.y < stair.y and lemming.x:
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
            
        for lemming in self.lemmings:
            if lemming.x <= self.gates.endgate_x + 10 and lemming.x >= self.gates.endgate_x - 10 and lemming.y >= self.gates.endgate_y - 5 and lemming.y <= self.gates.endgate_y + 5:
                lemming.saved = True
                self.saved[self.lemmings.index(lemming)] = True
        
        

    def update_platform(self, x, y, length, is_pl):
        for lemming in self.lemmings:
            if (lemming.x + 16 >= x
                and lemming.x <= x + length
                and lemming.y + 16 >= y
                and lemming.y + 16 <= y + 16):

                lemming.vy = 0
                lemming.fall = False

                if lemming.fell and pyxel.frame_count > 20 and not lemming.umbrella and not lemming.stairs:
                    lemming.alive = False
                    self.alive[self.lemmings.index(lemming)] = False
                    
            elif lemming.y + 16 >= y and lemming.y + 16 <= y + 16 and not lemming.stairs:
                if lemming.x + 16 < x or lemming.x > x + length:
                    lemming.fall = True
    
            if (lemming.y + 16 >= y
                and lemming.y <= y + 16
                and lemming.x + 12 == x):

                lemming.right = False
    
            if (lemming.y + 16 >= y
                and lemming.y <= y + 16
                and lemming.x == x + (length-6)):

                lemming.right = True

            if lemming.y > self.gates.startgate_y:
                lemming.fell = True

        return x, y, length, is_pl

    def draw(self):

        pyxel.cls(0)

        pyxel.text(3, 3, "Level: %i"%(level), 7)
        pyxel.text(59, 3, "Alive: %i"%(self.alive.count(True)), 7)
        pyxel.text(115, 3, "Saved: %i"%(self.saved.count(True)), 7)
        pyxel.text(171, 3, "Died: %i"%(self.alive.count(False)), 7)
        pyxel.text(3, 15, "Ladders: %i"%(len(self.stairs)), 7)
        pyxel.text(77, 15, "Umbrellas: %i"%(len(self.umbrellas)), 7)
        pyxel.text(151, 15, "Blockers: %i"%(len(self.platform)-7), 7)

        for x, y, length, is_pl in self.platform:
            if is_pl:
                for j in range(x, x+length, 16):
                    pyxel.blt(j, y, 0, 32, 0, 16, 16, colkey=0)

        pyxel.blt(self.gates.startgate_x, self.gates.startgate_y, 0, 0, 16, 16, 16, colkey=0)
        pyxel.blt(self.gates.endgate_x, self.gates.endgate_y, 0, 16, 16, 16, 16, colkey=0)
        # draw lemming
        animate = 0
        if pyxel.frame_count % 19 >= 0 and pyxel.frame_count % 19 < 5:
            animate = 0
        elif pyxel.frame_count % 19 >= 5 and pyxel.frame_count % 19 < 10:
            animate = 1
        elif pyxel.frame_count % 19 >= 10 and pyxel.frame_count % 19 < 15:
            animate = 2
        elif pyxel.frame_count % 19 >= 15 and pyxel.frame_count % 19 < 20:
            animate = 3
        for lemming in self.lemmings:
            if lemming.alive and not lemming.saved:
                if not lemming.umbrella and not lemming.blocker:
                    if lemming.right:
                        pyxel.blt(
                            lemming.x,
                            lemming.y,
                            1,
                            animate * 16,
                            0,
                            16,
                            16,
                            colkey=0
                            )
                    elif not lemming.right:
                        pyxel.blt(
                            lemming.x,
                            lemming.y,
                            1,
                            animate * 16,
                            16,
                            16,
                            16,
                            colkey=0
                            )
                elif lemming.umbrella and not lemming.blocker:
                    if lemming.right:
                        pyxel.blt(
                            lemming.x,
                            lemming.y,
                            1,
                            animate * 16,
                            64,
                            16,
                            16,
                            colkey=0
                            )
                    elif not lemming.right:
                        pyxel.blt(
                            lemming.x,
                            lemming.y,
                            1,
                            animate * 16,
                            96,
                            16,
                            16,
                            colkey=0
                            )
                elif lemming.blocker:
                    pyxel.blt(
                        lemming.x,
                        lemming.y,
                        1,
                        animate * 16,
                        48,
                        16,
                        16,
                        colkey=0
                        )
            elif not lemming.alive and not lemming.saved:
                self.animateDeath = 0
                if self.animateDeath < 5:
                    if pyxel.frame_count % 20 == 0:
                        self.animateDeath += 1
                    
                    pyxel.blt(
                            lemming.x,
                            lemming.y,
                            1,
                            animate *16 ,
                            80,
                            16,
                            16,
                            colkey=0
                            )
        pyxel.blt(self.cursor.x, self.cursor.y, 2, 16 if pyxel.frame_count % 30 < 15 else 0 , 48, 16, 16, colkey=0)
        for u in self.umbrellas:
            pyxel.blt(u.x, u.y, 2, 16 * animate , 16, 16, 16, colkey=0)
        for b in self.blockers:
            pyxel.blt(b.x, b.y, 0, 0 , 48, 16, 16, colkey=0)
        for s in self.stairs:
            if s.right:
                pyxel.blt(s.x, s.y, 2, 16 , 0, 16, 16, colkey=0)
            if not s.right:
                pyxel.blt(s.x, s.y, 2, 0 , 0, 16, 16, colkey=0)

plat = Platforms(platPos_x, platPos_y, platPos_w)
gat = Gates(plat, platPos_y)
lem = Lemmings(gat)
curs = Cursor()
PreGameHUD()
