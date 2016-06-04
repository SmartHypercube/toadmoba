# encoding=utf-8


'''
用方向键控制镜头，测试用
'''


import threading
from time import sleep, time

import pygame
from pygame.locals import *


class CameraCtrl:
    events = ['KeyDown', 'KeyUp']
    order = -100
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.x = 22*64
        self.y = 76*64
    @property
    def position(self):
        return (self.x, self.y)
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


camera = CameraCtrl()
eventCatchers = [camera]
running = False

def inthread(f):
    return threading.Thread(target=f).start

def init(modules, **env):
    pass

@inthread
def start():
    global running
    running = True
    while running:
        if camera.up:
            camera.y -= 10
        if camera.down:
            camera.y += 10
        if camera.left:
            camera.x -= 10
        if camera.right:
            camera.x += 10
        sleep(0.001)

def stop():
    global running
    running = False
