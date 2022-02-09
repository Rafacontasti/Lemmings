# -*- coding: utf-8 -*-

'''The platforms, represented as a matrix of rows equivalent to the number of
active platforms and four columns, the x and y coordenates for the columns,
the length of the columns and a "is_pl" boolean, respectively'''

# The platforms class


class Platforms:
    def __init__(self, platPos_x, platPos_y, platPos_w):
        self.platforms = []

        for n in range(len(platPos_x)):
            self.platforms.append([platPos_x[n],
                                   platPos_y[n],
                                   platPos_w[n],
                                   True])

    '''@property
    def platforms(self):
        return self.__platforms

    @platforms.setter
    def platforms(self, platPos_x: list, platPos_y: list, platPos_w: list):
        for x in platPos_x:
            if x < 0:
                platPos_x[x] = 0

        for y in platPos_y:
            if y < 0:
                platPos_y[y] = 0

        for w in platPos_w:
            if w < 0:
                platPos_x[w] = 0
        for n in range(len(platPos_x)):
            self.__platforms.append([platPos_x[n],
                                   platPos_y[n],
                                   platPos_w[n],
                                   True])'''
