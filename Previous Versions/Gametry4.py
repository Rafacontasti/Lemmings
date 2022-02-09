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
lemming_number = 4
lemmingslist = []
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
            self.endgate_x = int((platforms.platforms[random1_1][0]) + ((random2_2-5)*16))
            self.endgate_y = int((platforms.platforms[random1_1][1]) - 16)

        '''for i in range(len(platforms.platforms)):
            if platforms.platforms[i][1] == self.startgate_x:
                platforms.platforms.remove([platforms.platforms[i][0], platforms.platforms[i][1], platforms.platforms[i][2]], platforms.platforms[i][3])
                platPos_y.remove(platforms.platforms[i][1])
                while len(platforms.platforms) < 7:
                    randomz = random.randint(3, 15)*16
                    if randomz not in platPos_y:
                        platforms.platforms.append([platPos_x[n], platPos_y[n], platPos_w[n], True])'''

class Lemmings:
    def __init__(self, gates: Gates, lemmingslist):
        self.x = gates.startgate_x
        self.y = gates.startgate_y
        self.vy = 0
        self.fall = False
        self.right = True
        self.alive = True
        self.fell = False
        self.umbrella = False

    def update_lemming(self):
        if self.x == pyxel.width - 12:
            self.right = False
        if self.x == -4:
            self.right = True

        if not self.umbrella:
            if not self.right:
                self.x = self.x - .5
    
            if self.right:
                self.x = self.x + .5
        elif self.umbrella:
            if self.fall:
                self.x += .1
            elif not self.fall:
                self.x += .66
    
        self.y += self.vy
    
        if self.fall:
            if not self.umbrella:
                self.vy = self.vy + 1
            elif self.umbrella:
                self.y += .5
        else:
            self.vy = 0
    
        if self.y > pyxel.height and not self.umbrella:
            if self.alive:
                self.alive = False


class Cursor:
    def __init__(self):
        self.x = 112
        self.y = 144
    

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

class Umbrella:
    def __init__(self, cursor: Cursor):
        self.x = cursor.x
        self.y = cursor.y
    

class Game:
    def __init__(self, platforms: Platforms, gates: Gates, lemmings: Lemmings, cursor: Cursor):
        pyxel.init(WIDTH, HEIGHT, caption="Lemmings Game")

        pyxel.load("sprites.pyxres")

        self.lemmings = []
        self.gates = gates
        self.cursor = cursor
        self.umbrellas = []
        self.alive = []

        self.startgate = [gates.startgate_x, gates.startgate_y]
        self.endgate = [gates.endgate_x, gates.endgate_y]

        self.platform = platforms.platforms
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
        if pyxel.frame_count % 20 == 0 and len(self.lemmings) < lemming_number:
            self.lemmings.append(Lemmings(self.gates, self.lemmings))
            self.alive.append(True)

        for i in range(len(self.lemmings)):
            if not self.lemmings[i].alive:
                self.alive[i] = False
        
        for lemming in self.lemmings:
            lemming.update_lemming()

        for i, v in enumerate(self.platform):
            self.platform[i] = self.update_platform(*v)

        if pyxel.btn(pyxel.KEY_RIGHT) and self.cursor.x < pyxel.width - 16:
            self.cursor.x += 16
        if pyxel.btn(pyxel.KEY_LEFT) and self.cursor.x > 0:
            self.cursor.x -= 16
        if pyxel.btn(pyxel.KEY_UP) and self.cursor.y > 0:
            self.cursor.y -= 16
        if pyxel.btn(pyxel.KEY_DOWN) and self.cursor.y < pyxel.height - 16:
            self.cursor.y += 16

        if pyxel.btnp(pyxel.KEY_W):
            self.umbrellas.append(Umbrella(self.cursor))
        
        for umbrella in self.umbrellas:
            for lemming in self.lemmings:
                if lemming.y == umbrella.y and lemming.x == umbrella.x:
                    lemming.umbrella = True
                    self.umbrellas.remove(umbrella)
        
        lemmingslist = self.lemmings
    
    def update_platform(self, x, y, length, is_active):
        if is_active:
            for lemming in self.lemmings:
                if (lemming.x + 16 >= x
                    and lemming.x <= x + length
                    and lemming.y + 16 >= y
                    and lemming.y + 16 <= y + 16):

                    lemming.vy = 0
                    lemming.fall = False
                    if lemming.fell and pyxel.frame_count > 20 and not lemming.umbrella:
                        lemming.alive = False
                    
                elif lemming.y + 16 >= y and lemming.y + 16 <= y + 16:
                    if lemming.x + 16 < x or lemming.x > x + length:
                        lemming.fall = True
    
                if (lemming.y + 16 >= y
                    and lemming.y <= y + 16
                    and lemming.x + 12 == x):

                    lemming.right = False
    
                if (lemming.y+16 > y
                    and lemming.y <= y + 16
                    and lemming.x == x + (length-6)):

                    lemming.right = True

                if lemming.y > self.gates.startgate_y:
                    lemming.fell = True

        return x, y, length, is_active

    def draw(self):
        pyxel.cls(0)

        pyxel.text(3, 3, "Level: %i"%(level), 7)
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
        for lemming in self.lemmings:
            if lemming.alive:
                if not lemming.umbrella:
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
                elif lemming.umbrella:
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
            else:
                self.animateDeath = 0
                if self.animateDeath < 5:
                    if pyxel.frame_count % 20 == 0:
                        self.animateDeath += 1
                    
                    pyxel.blt(
                            lemming.x,
                            lemming.y,
                            1,
                            self.animateDeath *16 ,
                            80,
                            16,
                            16,
                            colkey=0
                            )
        pyxel.blt(self.cursor.x, self.cursor.y, 2, 16 if pyxel.frame_count % 30 < 15 else 0 , 48, 16, 16, colkey=0)
        for u in self.umbrellas:
            pyxel.blt(u.x, u.y, 2, 16 * animate , 16, 16, 16, colkey=0)

plat = Platforms(platPos_x, platPos_y, platPos_w)
gat = Gates(plat, platPos_y)
lem = Lemmings(gat, lemmingslist)
curs = Cursor()
PreGameHUD()
