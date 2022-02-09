# -*- coding: utf-8 -*-
import pyxel
from Game import Game

''' This is a file to contain the huds of the game'''


# A class for the welcoming screen, it shows the title and the creators, and
# runs the game
class PreGameHUD:
    def __init__(self, platforms, gates, cursor, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pyxel.init(self.WIDTH, self.HEIGHT, caption="Lemmings Game")
        pyxel.image(0).load(0, 0, "lemmingsTitle.png")

        self.platforms = platforms
        self.gates = gates
        self.cursor = cursor

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.quit()
            Game(self.platforms, self.gates, self.cursor)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(16, 96, 0, 0, 0, 192, 64)
        colortext = pyxel.frame_count % 25
        pyxel.text(69, 151, "Press ENTER to start", 7 if colortext < 10 else 0)
        pyxel.text(0, pyxel.height - 16,
                   "          By Rafael Contasti and Carlos Iborra", 7)
