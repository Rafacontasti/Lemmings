# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:55:10 2020

@author: Rafael Contasti

Game try 2.0
"""

import pyxel
import random
WIDTH = 224
HEIGHT = 256
platPos_x = []
platPos_y = []
platPos_w = []

for w in range(7):
    platPos_w.append(16*random.randint(5, 10))

for w in range(7):
    randomx = (random.randint(0, 9)*16)
    while randomx + platPos_w[w] > 211:
        randomx -= 16
    platPos_x.append(randomx)

while len(platPos_y) < 7:
    randomx = random.randint(3, 16)
    if randomx*16 not in platPos_y:
        platPos_y.append(randomx*16)

class Platforms:
    def __init__(self, platPos_x, platPos_y, platPos_w):
        self.platforms = []
        for n in range(len(platPos_x)):
            self.platforms.append([platPos_x[n],
                                   platPos_y[n],
                                   platPos_w[n],
                                   True])

class Gates:
    def __init__(self, platforms: Platforms):
        random1 = random.randint(0, 6)
        random2 = random.randint(5, ((platforms.platforms[random1][2])/16))
        print(random2)
        self.startgate_x = (platforms.platforms[random1][0]) + ((random2-5)*16)
        self.startgate_y = (platforms.platforms[random1][1]) - 16
        self.endgate_x = (platforms.platforms[random1][0]) + ((random2-5)*16)
        self.endgate_y =(platforms.platforms[random1][1]) - 16

class Lemmings:
    def __init__(self, gates: Gates):
        self.lemming_number = 3
        self.lemming_x = []
        self.lemming_y = []
        self.lemming_vy = []
        self.lemming_fall = []
        self.lemming_right = []
        self.lemming_is_alive = []
        
        for f in range(self.lemming_number):
            self.lemming_x.append(gates.startgate_x)
            self.lemming_y.append(gates.startgate_y)
            self.lemming_vy.append(0)
            self.lemming_fall.append(True)
            self.lemming_right.append(True)
            self.lemming_is_alive.append(True)

class Game:
    def __init__(self, platforms: Platforms, gates: Gates, lemmings: Lemmings):
        pyxel.init(WIDTH, HEIGHT, caption="Lemmings Game")

        pyxel.image(1).load(17, 0, "assets/tierrita.png")
        pyxel.image(0).load(17, 0, "assets/lemming.png")
        pyxel.image(2).load(17, 0, "assets/door.png")
        pyxel.image(2).load(1, 0, "assets/finaldoor.png")

        self.lemming_x = lemmings.lemming_x
        self.lemming_y = lemmings.lemming_y
        self.lemming_vy = lemmings.lemming_vy
        self.lemming_fall = lemmings.lemming_fall
        self.lemming_right = lemmings.lemming_right
        self.lemming_is_alive = lemmings.lemming_is_alive
        print(self.lemming_x)

        self.startgate = [gates.startgate_x, gates.startgate_y]
        self.endgate = [gates.endgate_x, gates.endgate_y]

        self.platform = platforms.platforms
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.update_lemming()

        for i, v in enumerate(self.platform):
            self.platform[i] = self.update_platform(*v)

    def update_lemming(self):
        for s in range(len(self.lemming_x)):
            if self.lemming_x[s] == pyxel.width - 12:
                self.lemming_right[s] = False
    
            if self.lemming_x[s] == -4:
                self.lemming_right[s] = True
    
            if not self.lemming_right[s]:
                self.lemming_x[s] = self.lemming_x[s] - 1
    
            if self.lemming_right[s]:
                self.lemming_x[s] = self.lemming_x[s] + 1
    
            self.lemming_y[s] += self.lemming_vy[s]
    
            if self.lemming_fall[s]:
                self.lemming_vy[s] = self.lemming_vy[s] + 1
            else:
                self.lemming_vy[s] = 0
    
            if self.lemming_y[s] > pyxel.height:
                if self.lemming_is_alive[s]:
                    self.lemming_is_alive[s] = False

    def update_platform(self, x, y, length, is_active):
        if is_active:
            for g in range(len(self.lemming_x)):
                if (
                    self.lemming_x[g] + 16 >= x
                    and self.lemming_x[g] <= x + length
                    and self.lemming_y[g] + 16 >= y
                    and self.lemming_y[g] <= y + 16
    
                ):
                    self.lemming_vy[g] = 0
                    self.lemming_fall[g] = False
    
                else:
                    self.lemming_fall[g] = True
    
                if (
                    self.lemming_y[g]+16 > y
                    and self.lemming_y[g] <= y + 16
                    and self.lemming_x[g]+16 == x
                ):
                    self.lemming_right[g] = False
    
                if (
                    self.lemming_y[g]+16 > y
                    and self.lemming_y[g] <= y + 16
                    and self.lemming_x[g] == x + length
                ):
                    self.lemming_right[g] = True

        return x, y, length, is_active

    def draw(self):
        pyxel.cls(0)

        pyxel.text(3, 3, "Level: ", 7)
        pyxel.text(54, 3, "Alive: ", 7)
        pyxel.text(108, 3, "Saved: ", 7)
        pyxel.text(162, 3, "Died: ", 7)
        pyxel.text(3, 15, "Ladders: ", 7)
        pyxel.text(73, 15, "Umbrellas: ", 7)
        pyxel.text(143, 15, "Blockers: ", 7)

        for i in range(0, pyxel.width, int(pyxel.width/14)):
            for j in range(32, pyxel.height, int(pyxel.width/14)):
                pyxel.rectb(i, j, 16, 16, 7)

        for x, y, length, is_active in self.platform:
            for j in range(x, x+length, 16):
                pyxel.blt(j, y, 1, 17, 0, 16, 16, colkey=0)

        pyxel.blt(self.startgate[0], self.startgate[1], 2, 17, 0, 16, 16)
        pyxel.blt(self.endgate[0], self.endgate[1], 2, 17, 0, 16, 16)
        # draw lemming
        for h in range(len(self.lemming_x)):
            pyxel.blt(
                self.lemming_x[h],
                self.lemming_y[h
                               ],
                0,
                16,
                0,
                16,
                16
            )


plat = Platforms(platPos_x, platPos_y, platPos_w)
gat = Gates(plat)
lem = Lemmings(gat)
Game(plat, gat, lem)
