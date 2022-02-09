# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:44:33 2020

@author: Rafael Contasti
"""
import pyxel


class Game:
    def __init__(self):
        pyxel.init(211, 241, caption="Lemmings Game")

        pyxel.image(1).load(17, 0, "assets/tierrita.png")
        pyxel.image(0).load(17, 0, "assets/lemming.png")
        self.lemming_x = 1
        self.lemming_y = 0
        self.lemming_vy = 0
        self.lemming_fall = True
        self.lemming_right = True
        self.lemming_is_alive = True

        self.platform = [[0, 6*15, 5*15, True], [0*15, 15*12, 10*15, True], [15*10, 15*13, 5*15, True], [5*15, 7*15, 3*15, True]]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_lemming()

        for i, v in enumerate(self.platform):
            self.platform[i] = self.update_platform(*v)

    def update_lemming(self):
        if self.lemming_x == pyxel.width - 16:
            self.lemming_right = False

        if self.lemming_x == 0:
            self.lemming_right = True

        if not self.lemming_right:
            self.lemming_x = self.lemming_x - 1

        if self.lemming_right:
            self.lemming_x = self.lemming_x + 1

        self.lemming_y += self.lemming_vy

        if self.lemming_fall:
            self.lemming_vy = self.lemming_vy + 1
        else:
            self.lemming_vy = 0

        if self.lemming_y > pyxel.height:
            if self.lemming_is_alive:
                self.lemming_is_alive = False

    def update_platform(self, x, y, length, is_active):
        if is_active:
            if (
                self.lemming_x + 16 >= x
                and self.lemming_x <= x + length
                and self.lemming_y + 16 >= y
                and self.lemming_y <= y + 16

            ):
                self.lemming_vy = 0
                self.lemming_fall = False

            else:
                self.lemming_fall = True

            if (
                self.lemming_y+16 > y
                and self.lemming_y <= y + 16
                and self.lemming_x+16 == x
            ):
                self.lemming_right = False

            if (
                self.lemming_y+16 > y
                and self.lemming_y <= y + 16
                and self.lemming_x == x + length
            ):
                self.lemming_right = True

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

        for i in range(0, 211, 15):
            for j in range(30, 241, 15):
                pyxel.rectb(i, j, 16, 16, 7)

        for x, y, length, is_active in self.platform:
            for j in range(x, x+length, 15):
                pyxel.blt(j, y, 1, 17, 0, 16, 16)

        # draw player
        pyxel.blt(
            self.lemming_x,
            self.lemming_y,
            0,
            16,
            0,
            16,
            16
        )


Game()
