# encoding=utf-8


'''
按ESC键退出，测试用
'''


import pygame
from pygame.locals import *


class EscQuitter:
    events = ['KeyUp']
    order = -100
    def isInside(self, pos):
        return False
    def onEvent(self, event, data, mouseOn=None):
        if data.key == K_ESCAPE:
            envstop()
            return True
        return False


eventCatchers = [EscQuitter()]
def init(modules, **env):
    global envstop
    envstop = env['stop']
start = lambda: None
stop = lambda: None
