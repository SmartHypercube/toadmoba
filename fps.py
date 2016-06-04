# encoding=utf-8


'''
显示实时FPS
'''


from time import time

import pygame
from pygame.locals import *


class Fps:
    order = 0
    def __init__(self):
        self.font = pygame.font.Font('font/wqy-microhei.ttc', 18)
        self.oldtime = 0
    def draw(self, cameraPos, windowMid, surf):
        newtime = time()
        dt = newtime - self.oldtime
        fps = 1 // dt
        text = self.font.render('%d' % fps, True, (255, 255, 255))
        rect = text.get_rect()
        rect.topleft = (0, 0)
        surf.blit(text, rect)
        self.oldtime = newtime


characters = [Fps()]

def init(modules, **env):
    pass

def start():
    pass

def stop():
    pass
