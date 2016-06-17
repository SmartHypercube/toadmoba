# encoding=utf-8


'''
玩家控制

接收全局事件，进行寻路及其他计算，控制玩家角色

存在待控制角色的模块，应提供：
    main_character : <Character>

<Character>应提供：
    position : Vector2
'''


import threading
from time import sleep

import pygame
from pygame.locals import *
from pygame.math import Vector2


vasint = lambda v: (int(v.x), int(v.y))


class _: events = []
BLANK = _()


class Control:
    '''暂且由Control也负责camera'''
    events = ['KeyDown', 'KeyUp', 'GlobalMouseButtonUp']
    order = -100
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self._character = None
    @property
    def character(self):
        return self._character
    @character.setter
    def character(self, value):
        self._character = value
        self.target = value.position
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
        if event.startswith('Key'):
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
        # mouseOn是被点击的目标
        targetType = mouseOn.mouseOnType(self.character)
        if targetType == 'moveto':
            self.target = mouseOn.mouseOnPos()


control = Control()
camera = control
eventCatchers = [control]
def init(modules, **env):
    for module in modules:
        try: control.character = module.main_character
        except: pass


def inthread(f):
    return threading.Thread(target=f).start

running = False

@inthread
def start():
    global running
    running = True
    while running:
        r, phi = (camera.position - camera.target).as_polar()
        if r >= 2:
            camera.position += 2*(camera.target - camera.position).normalize()
            camera.character.angle = 180-phi
        sleep(0.01)

def stop():
    global running
    running = False
