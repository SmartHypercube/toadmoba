# encoding=utf-8


'''
所有游戏中单位
'''


import threading
from time import sleep

import pygame
from pygame.locals import *
from pygame.math import Vector2


vasint = lambda v: (int(v.x), int(v.y))


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


class 单位:

    name = '单位'
    events = ['MouseEnter', 'MouseLeave', 'GlobalMouseButtonDown', 'MouseButtonUp']

    def __init__(self, team, position):
        self.position = position * 64
        self.team = team
        self.img_r = loadimage('images/%s_r.png' % self.name)
        transparent(self.img_r)
        self.img_m = loadimage('images/%s_m.png' % self.name)
        transparent(self.img_m)
        self.img_s = loadimage('images/%s_s.png' % self.name)
        transparent(self.img_s)
        self.useimg = self.img_r
        self.size = Vector2(self.img_r.get_size())
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
        raise NotImplementedError

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
        pos = Vector2(pos)
        pos += self.cameraPos - self.windowMid - self.position + self.size // 2
        if not pos.elementwise() >= 0:
            return False
        if not pos.elementwise() < self.useimg.get_size():
            return False
        return self.useimg.get_at(vasint(pos)).a != 0


class 建筑(单位):

    def __init__(self, team, position, angle):
        单位.__init__(self, team, position)
        self.angle = angle
        self.img_r = pygame.transform.rotate(self.img_r, angle)
        self.img_m = pygame.transform.rotate(self.img_m, angle)
        self.img_s = pygame.transform.rotate(self.img_s, angle)
        self.rect = self.img_r.get_rect()

    def draw(self, cameraPos, windowMid, surf):
        self.cameraPos = cameraPos
        self.windowMid = windowMid
        self.rect.center = vasint(self.position - cameraPos + windowMid)
        surf.blit(self.img, self.rect)
        self.useimg = self.img


class 英雄(单位):

    def __init__(self, team, position, angle):
        单位.__init__(self, team, position)
        self.angle = angle

    def draw(self, cameraPos, windowMid, surf):
        self.cameraPos = cameraPos
        self.windowMid = windowMid
        img = pygame.transform.rotate(self.img, self.angle)
        rect = img.get_rect()
        rect.center = vasint(self.position - cameraPos + windowMid)
        surf.blit(img, rect)
        self.useimg = img
        self.rect = rect


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
        self.position += (32, 32)


class 主角(英雄):

    name = '主角'


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


class Camera:
    events = ['KeyDown', 'KeyUp']
    order = -100
    def __init__(self, character):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.character = character
    @property
    def position(self):
        return Vector2(self.character.position)
    @position.setter
    def position(self, value):
        self.character.position = value
    def draw(self, cameraPos, windowMid, surf):
        pass
    def isInside(self, pos):
        return False
    def onEvent(self, event, data, mouseOn=None):
        if data.key == K_UP:
            self.up = event == 'KeyDown'
        elif data.key == K_DOWN:
            self.down = event == 'KeyDown'
        elif data.key == K_LEFT:
            self.left = event == 'KeyDown'
        elif data.key == K_RIGHT:
            self.right = event == 'KeyDown'
        else:
            return False
        return True


_主角 = 主角(1, Vector2(20, 79), 45)
camera = Camera(_主角)
characters = [建筑层, 英雄层, 野怪层, 小兵层]
eventCatchers = [建筑层, 英雄层, 野怪层, 小兵层, camera]
def init(modules, **env):
    建筑层.units.extend([
            泉水塔  (1, Vector2(14, 85), 0),
            水晶枢纽(1, Vector2(22, 76), 0),
            门牙塔  (1, Vector2(23, 74), 0),
            门牙塔  (1, Vector2(25, 76), 0),
            #水晶    (1, Vector2(21, 68), 270),
            #水晶    (1, Vector2(30, 69), 315),
            #水晶    (1, Vector2(31, 78), 0),
            高地塔  (1, Vector2(21, 64), 270),
            内塔    (1, Vector2(22, 52), 270),
            外塔    (1, Vector2(20, 35), 270),
            高地塔  (1, Vector2(33, 66), 315),
            内塔    (1, Vector2(38, 62), 315),
            外塔    (1, Vector2(42, 56), 315),
            高地塔  (1, Vector2(35, 78), 0),
            内塔    (1, Vector2(47, 77), 0),
            外塔    (1, Vector2(64, 79), 0),
            泉水塔  (2, Vector2(85, 14), 180),
            水晶枢纽(2, Vector2(76, 22), 180),
            门牙塔  (2, Vector2(74, 23), 180),
            门牙塔  (2, Vector2(76, 25), 180),
            #水晶    (2, Vector2(68, 21), 180),
            #水晶    (2, Vector2(69, 30), 135),
            #水晶    (2, Vector2(78, 31), 90),
            高地塔  (2, Vector2(64, 21), 180),
            内塔    (2, Vector2(52, 22), 180),
            外塔    (2, Vector2(35, 20), 180),
            高地塔  (2, Vector2(66, 33), 135),
            内塔    (2, Vector2(62, 38), 135),
            外塔    (2, Vector2(56, 42), 135),
            高地塔  (2, Vector2(78, 35), 90),
            内塔    (2, Vector2(77, 47), 90),
            外塔    (2, Vector2(79, 64), 90)
    ])
    英雄层.units.extend([_主角])


def inthread(f):
    return threading.Thread(target=f).start

running = False

@inthread
def start():
    global running
    running = True
    while running:
        if camera.up:
            camera.position += (0, -10)
        if camera.down:
            camera.position += (0, 10)
        if camera.left:
            camera.position += (-10, 0)
        if camera.right:
            camera.position += (10, 0)
        sleep(0.01)

def stop():
    global running
    running = False
