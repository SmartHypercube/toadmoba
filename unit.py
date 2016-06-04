# encoding=utf-8


'''
所有游戏中单位
'''


import pygame
from pygame.locals import *


class _: events = []
BLANK = _()


屏幕信息_L = 0
特效_L = 10
建筑_L = 20
英雄_L = 30
野怪_L = 40
小兵_L = 50
地图_L = 100
SCALE = 64


def loadimage(path):
    return pygame.image.load(path.encode()).convert(32, SRCALPHA)
def transparent(surf):
    topleft = surf.get_at((0, 0))
    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            if surf.get_at((x, y)) == topleft:
                surf.set_at((x, y), (0, 0, 0, 0))


class 建筑:

    name = '建筑'
    events = ['MouseEnter', 'MouseLeave', 'GlobalMouseButtonDown', 'MouseButtonUp']

    def __init__(self, team, position, angle):
        self.team = team
        self.x, self.y = position
        self.x *= 64
        self.y *= 64
        self.position = (self.x, self.y)
        self.angle = angle
        self.img_r = loadimage('images/%s%d_r.png' % (self.name, team))
        transparent(self.img_r)
        self.img_r = pygame.transform.rotate(self.img_r, angle)
        self.img_m = loadimage('images/%s%d_m.png' % (self.name, team))
        transparent(self.img_m)
        self.img_m = pygame.transform.rotate(self.img_m, angle)
        self.img_s = loadimage('images/%s%d_s.png' % (self.name, team))
        transparent(self.img_s)
        self.img_s = pygame.transform.rotate(self.img_s, angle)
        self.rect = self.img_r.get_rect()
        self.radius = max(self.rect.size) // 2
        self._mouseOn = False
        self._selected = False
        self.mouseOn = False
        self.selected = False

    @property
    def mouseOn(self):
        return self._mouseOn

    @mouseOn.setter
    def mouseOn(self, value):
        self._mouseOn = value
        if not self.selected:
            self.img = self.img_m if value else self.img_r

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        if value:
            self.img = self.img_s
        else:
            self.img = self.img_m if self.mouseOn else self.img_r

    def draw(self, cameraPos, windowMid, surf):
        self.cameraPos = cameraPos
        self.windowMid = windowMid
        cameraX, cameraY = cameraPos
        windowMidX, windowMidY = windowMid
        if abs(self.x - cameraX) > windowMidX + self.radius:
            return
        if abs(self.y - cameraY) > windowMidY + self.radius:
            return
        self.rect.center = (self.x - cameraX + windowMidX,
                self.y - cameraY + windowMidY)
        surf.blit(self.img, self.rect)

    def onEvent(self, event, data, mouseOn=None):
        if event == 'MouseEnter':
            self.mouseOn = True
        elif event == 'MouseLeave':
            self.mouseOn = False
        elif event == 'GlobalMouseButtonDown':
            self.selected = False
        elif event == 'MouseButtonUp':
            self.selected = True

    def isInside(self, pos):
        x = pos[0] - self.windowMid[0] + self.cameraPos[0] - self.x + \
                self.rect.width // 2
        if x not in range(self.img.get_width()):
            return False
        y = pos[1] - self.windowMid[1] + self.cameraPos[1] - self.y + \
                self.rect.height // 2
        if y not in range(self.img.get_height()):
            return False
        return self.img.get_at((x, y)).a != 0


class 泉水塔(建筑):

    name = '泉水塔'


class 门牙塔(建筑):

    name = '泉水塔'


class 高地塔(建筑):

    name = '泉水塔'


class 内塔(建筑):

    name = '泉水塔'


class 外塔(建筑):

    name = '泉水塔'


class 水晶枢纽(建筑):

    name = '水晶枢纽'

    def __init__(self, team, position, angle):
        建筑.__init__(self, team, position, angle)
        self.x += 32
        self.y += 32


class Layer:
    events = ['MouseEnter', 'MouseLeave', 'MouseButtonUp', 'GlobalMouseButtonDown']
    def __init__(self, order, units):
        self.order = order
        self.units = units
        self.mouseOn = BLANK
    def draw(self, cameraPos, windowMid, surf):
        for unit in self.units:
            unit.draw(cameraPos, windowMid, surf)
    def isInside(self, pos):
        if self.mouseOn is not BLANK and self.mouseOn.isInside(pos):
            return True
        if 'MouseLeave' in self.mouseOn.events:
            self.mouseOn.onEvent('MouseLeave', pos)
        self.mouseOn = BLANK
        for unit in self.units:
            if unit.isInside(pos):
                self.mouseOn = unit
                if 'MouseEnter' in self.mouseOn.events:
                    self.mouseOn.onEvent('MouseEnter', pos)
                return True
        return False
    def onEvent(self, event, data, mouseOn=None):
        if event.startswith('Mouse'):
            if event in self.mouseOn.events:
                self.mouseOn.onEvent(event, data, self.mouseOn)
        elif event.startswith('Global'):
            for unit in self.units:
                if event in unit.events:
                    unit.onEvent(event, data, mouseOn)

建筑层 = Layer(建筑_L, [])

英雄层 = Layer(英雄_L, [])

野怪层 = Layer(野怪_L, [])

小兵层 = Layer(小兵_L, [])


characters = [建筑层, 英雄层, 野怪层, 小兵层]
#camera = 建筑层.units[1]
eventCatchers = [建筑层, 英雄层, 野怪层, 小兵层]
def init(modules, **env):
    建筑层.units.extend([
            泉水塔  (1, (14, 85), 0),
            水晶枢纽(1, (22, 76), 0),
            门牙塔  (1, (23, 74), 0),
            门牙塔  (1, (25, 76), 0),
            #水晶    (1, (21, 68), 270),
            #水晶    (1, (30, 69), 315),
            #水晶    (1, (31, 78), 0),
            高地塔  (1, (21, 64), 270),
            内塔    (1, (22, 52), 270),
            外塔    (1, (20, 35), 270),
            高地塔  (1, (33, 66), 315),
            内塔    (1, (38, 62), 315),
            外塔    (1, (42, 56), 315),
            高地塔  (1, (35, 78), 0),
            内塔    (1, (47, 77), 0),
            外塔    (1, (64, 79), 0),
            泉水塔  (2, (85, 14), 180),
            水晶枢纽(2, (76, 22), 180),
            门牙塔  (2, (74, 23), 180),
            门牙塔  (2, (76, 25), 180),
            #水晶    (2, (68, 21), 180),
            #水晶    (2, (69, 30), 135),
            #水晶    (2, (78, 31), 90),
            高地塔  (2, (64, 21), 180),
            内塔    (2, (52, 22), 180),
            外塔    (2, (35, 20), 180),
            高地塔  (2, (66, 33), 135),
            内塔    (2, (62, 38), 135),
            外塔    (2, (56, 42), 135),
            高地塔  (2, (78, 35), 90),
            内塔    (2, (77, 47), 90),
            外塔    (2, (79, 64), 90)
    ])
start = lambda: None
stop = lambda: None
