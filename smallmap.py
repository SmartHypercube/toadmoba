# encoding=utf-8


'''
小地图
'''


import pygame
from pygame.locals import *
from pygame.math import Vector2


vasint = lambda v: (int(v.x), int(v.y))


屏幕信息_L = 0


class Map:

    events = ['MouseButtonDown', 'GlobalMouseButtonDown']

    def __init__(self):
        self.order = 屏幕信息_L
        self.design = pygame.transform.scale(pygame.image.load('images/mapdesign.png'), (300, 300))
        self.rect = self.design.get_rect()
        self.target = Vector2(0, 0)

    def draw(self, cameraPos, windowMid, surf):
        self.cameraPos = cameraPos
        self.windowMid = windowMid
        self.rect.bottomright = vasint(2*windowMid)
        surf.blit(self.design, self.rect)

    def isInside(self, pos):
        return pos[0] > self.rect.left and pos[1] > self.rect.top

    def onEvent(self, event, data, mouseOn=None):
        if event == 'GlobalMouseButtonDown':
            if mouseOn == self:
                return
            self.target = Vector2(0, 0)
            return
        self.target = (Vector2(data.pos) - (1, 1) - Vector2(self.rect.topleft)) *64/3

    def mouseOnType(self, player):
        return 'moveto'

    def mouseOnPos(self):
        return self.target


map = Map()
characters = [map]
eventCatchers = [map]
def init(modules, **env):
    pass
start = lambda: None
stop = lambda: None
