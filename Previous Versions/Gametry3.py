# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:55:10 2020

@author: Rafael Contasti

Game try 2.0
"""

import pyxel
import random
import time

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
    randomx = random.randint(3, 15)
    if randomx*16 not in platPos_y:
        platPos_y.append(randomx*16)

class Platforms:
    def __init__(self, platPos_x, platPos_y, platPos_w):
        self.platforms = []
        self.freePlatforms = []

        for n in range(len(platPos_x)):
            self.platforms.append([platPos_x[n],
                                   platPos_y[n],
                                   platPos_w[n],
                                   True])
        for pl in platPos_y:
            if pl+16 not in platPos_y:
                self.freePlatforms.append(pl+16)
        

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
            self.endgate_x = (platforms.platforms[random1_1][0]) + ((random2_2-5)*16)
            self.endgate_y = (platforms.platforms[random1_1][1]) - 16

        '''for i in range(len(platforms.platforms)):
            if platforms.platforms[i][1] == self.startgate_x:
                platforms.platforms.remove([platforms.platforms[i][0], platforms.platforms[i][1], platforms.platforms[i][2]], platforms.platforms[i][3])
                platPos_y.remove(platforms.platforms[i][1])
                while len(platforms.platforms) < 7:
                    randomz = random.randint(3, 15)*16
                    if randomz not in platPos_y:
                        platforms.platforms.append([platPos_x[n], platPos_y[n], platPos_w[n], True])'''

class Lemmings:
    def __init__(self, gates: Gates):
        self.lemming_number = 4
        self.lemming_x = []
        self.lemming_y = []
        self.lemming_vy = []
        self.lemming_fall = []
        self.lemming_right = []
        self.lemming_is_alive = []
        self.lemmingfell = []
        self.lemming_umbrella = []

    def update_lemming(self):
        for s in range(len(self.lemming_x)):
            if self.lemming_x[s] == pyxel.width - 12:
                self.lemming_right[s] = False
    
            if self.lemming_x[s] == -4:
                self.lemming_right[s] = True
    
            if not self.lemming_right[s]:
                self.lemming_x[s] = self.lemming_x[s] - .66
    
            if self.lemming_right[s]:
                self.lemming_x[s] = self.lemming_x[s] + .66
    
            self.lemming_y[s] += self.lemming_vy[s]
    
            if self.lemming_fall[s]:
                self.lemming_vy[s] = self.lemming_vy[s] + 1
            else:
                self.lemming_vy[s] = 0
    
            if self.lemming_y[s] > pyxel.height:
                if self.lemming_is_alive[s]:
                    self.lemming_is_alive[s] = False

class Cursor:
    def __init__(self):
        self.cursor_x = 112
        self.cursor_y = 144

class PreGameHUD:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, caption="Lemmings Game")
        pyxel.image(0).load(0, 0, "assets/lemmingsTitle.png")

        pyxel.run(self.update, self.draw)
    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            Game(plat, gat, lem, curs)
            pyxel.quit()
    def draw(self):
        pyxel.cls(0)
        pyxel.blt(16, 96, 0, 0, 0, 192, 64)
        colortext = pyxel.frame_count % 25
        pyxel.text(69, 151, "Press ENTER to start", 7 if colortext < 10 else 0)
        pyxel.text(0, pyxel.height - 16, "          By Rafael Contasti and Carlos Iborra", 7)


class Game:
    def __init__(self, platforms: Platforms, gates: Gates, lemmings: Lemmings, cursor: Cursor):
        pyxel.init(WIDTH, HEIGHT, caption="Lemmings Game")

        pyxel.load("sprites.pyxres")

        self.lemming_x = lemmings.lemming_x
        self.lemming_y = lemmings.lemming_y
        self.lemming_vy = lemmings.lemming_vy
        self.lemming_fall = lemmings.lemming_fall
        self.lemming_right = lemmings.lemming_right
        self.lemming_is_alive = lemmings.lemming_is_alive
        self.lemmingsvar = lemmings
        self.lemmingCounter = 0
        self.lemmingfell = lemmings.lemmingfell
        self.deathtime = []
        self.lemming_umbrella = lemmings.lemming_umbrella
        self.cursor_x = 112
        self.cursor_y = 144

        self.startgate = [gates.startgate_x, gates.startgate_y]
        self.endgate = [gates.endgate_x, gates.endgate_y]

        self.platform = platforms.platforms
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
        if pyxel.frame_count % 20 == 0 and self.lemmingCounter < self.lemmingsvar.lemming_number:
            self.lemming_x.append(self.startgate[0])
            self.lemming_y.append(self.startgate[1])
            self.lemming_vy.append(0)
            self.lemming_fall.append(False)
            self.lemming_right.append(True)
            self.lemming_is_alive.append(True)
            self.lemmingfell.append(False)
            self.lemmingCounter += 1
        
        self.lemmingsvar.update_lemming()

        for i, v in enumerate(self.platform):
            self.platform[i] = self.update_platform(*v)

        if pyxel.btn(pyxel.KEY_RIGHT) and self.cursor_x < pyxel.width - 16:
            self.cursor_x += 16
        if pyxel.btn(pyxel.KEY_LEFT) and self.cursor_x > 0:
            self.cursor_x -= 16
        if pyxel.btn(pyxel.KEY_UP) and self.cursor_y > 0:
            self.cursor_y -= 16
        if pyxel.btn(pyxel.KEY_DOWN) and self.cursor_y < pyxel.height - 16:
            self.cursor_y += 16
    
    def update_platform(self, x, y, length, is_active):
        if is_active:
            for g in range(len(self.lemming_x)):
                if (
                    self.lemming_x[g] + 16 >= x
                    and self.lemming_x[g] <= x + length
                    and self.lemming_y[g] + 16 >= y
                    and self.lemming_y[g] + 16 <= y + 16
    
                ):
                    self.lemming_vy[g] = 0
                    self.lemming_fall[g] = False
                    if self.lemmingfell[g] and pyxel.frame_count > 20:
                        self.lemming_is_alive[g] = False
                        self.deathtime.append(time.time())
    
                else:
                    self.lemming_fall[g] = True
    
                if (
                    self.lemming_y[g]+16 >= y
                    and self.lemming_y[g] <= y + 16
                    and self.lemming_x[g]+12 == x
                ):
                    self.lemming_right[g] = False
    
                if (
                    self.lemming_y[g]+16 > y
                    and self.lemming_y[g] <= y + 16
                    and self.lemming_x[g] == x + (length-6)
                ):
                    self.lemming_right[g] = True
                for i in range(len(self.lemming_fall)):
                    if self.lemming_y[i] > self.startgate[1]:
                        self.lemmingfell[i] = True

        return x, y, length, is_active

    def draw(self):
        pyxel.cls(0)

        pyxel.text(3, 3, "Level: ", 7)
        pyxel.text(59, 3, "Alive: ", 7)
        pyxel.text(115, 3, "Saved: ", 7)
        pyxel.text(171, 3, "Died: ", 7)
        pyxel.text(3, 15, "Ladders: ", 7)
        pyxel.text(77, 15, "Umbrellas: ", 7)
        pyxel.text(151, 15, "Blockers: ", 7)

        '''for i in range(0, pyxel.width, int(pyxel.width/14)):
            for j in range(32, pyxel.height, int(pyxel.width/14)):
                pyxel.rectb(i, j, 16, 16, 7)'''

        for x, y, length, is_active in self.platform:
            for j in range(x, x+length, 16):
                pyxel.blt(j, y, 0, 32, 0, 16, 16, colkey=0)

        pyxel.blt(self.startgate[0], self.startgate[1], 0, 0, 16, 16, 16, colkey=0)
        pyxel.blt(self.endgate[0], self.endgate[1], 0, 16, 16, 16, 16, colkey=0)
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
        for h in range(len(self.lemming_x)):
            if self.lemming_is_alive[h]:
                if self.lemming_right[h]:
                    pyxel.blt(
                        self.lemming_x[h],
                        self.lemming_y[h],
                        1,
                        animate * 16,
                        0,
                        16,
                        16,
                        colkey=0
                        )
                elif not self.lemming_right[h]:
                    pyxel.blt(
                        self.lemming_x[h],
                        self.lemming_y[h],
                        1,
                        animate * 16,
                        16,
                        16,
                        16,
                        colkey=0
                        )
            else:
                self.animateDeath = 0
                if self.animateDeath < 5:
                    if pyxel.frame_count % 20 == 0:
                        self.animateDeath += 1
                    
                    pyxel.blt(
                            self.lemming_x[h],
                            self.lemming_y[h],
                            1,
                            self.animateDeath *16 ,
                            80,
                            16,
                            16,
                            colkey=0
                            )
        pyxel.blt(self.cursor_x, self.cursor_y, 2, 16 if pyxel.frame_count % 30 < 15 else 0 , 48, 16, 16, colkey=0)


plat = Platforms(platPos_x, platPos_y, platPos_w)
gat = Gates(plat, platPos_y)
lem = Lemmings(gat)
curs = Cursor()
PreGameHUD()
