# encoding=utf-8


'''
地图
'''


import pygame
from pygame.locals import *
from pygame.math import Vector2


vasint = lambda v: (int(v.x), int(v.y))


地图_L = 100

C_OUTSIDE  = (127, 127, 127) # 地图外侧
C_SIDE     = (  0,   0,   0) # 墙
C_GROUND   = (255, 255, 255) # 地面
C_BUILDING = (237,  28,  36) # 建筑
C_JUNGLE   = (195, 195, 195) # 野区
C_NEUTRAL  = ( 63,  72, 204) # 野怪
C_GRASS    = ( 34, 177,  76) # 草丛
C_RIVER    = (153, 217, 234) # 河道

MATERIALS = {
        C_OUTSIDE : ( 64, 0, 64, 64), # 圆石
        C_SIDE    : ( 64, 0, 64, 64), # 圆石
        C_GROUND  : (128, 0, 64, 64), # 石头
        C_BUILDING: (128, 0, 64, 64), # 石头
        C_JUNGLE  : (  0, 0, 64, 64), # 泥土
        C_NEUTRAL : (  0, 0, 64, 64), # 泥土
        C_GRASS   : (192, 0, 64, 64), # 草地
        C_RIVER   : (256, 0, 64, 64)  # 水
}

m_rect = Rect((0, 0, 64, 64))

def transparent(surf):
    topleft = surf.get_at((0, 0))
    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            if surf.get_at((x, y)) == topleft:
                surf.set_at((x, y), (0, 0, 0, 0))

class Map:

    events = ['MouseButtonDown', 'GlobalMouseButtonDown']

    def __init__(self):
        self.order = 地图_L
        self.design = pygame.image.load('images/mapdesign.png')
        material = pygame.image.load('images/mud_rock_stone_grass_water.png').convert()
        for m in MATERIALS:
            MATERIALS[m] = material.subsurface(Rect(MATERIALS[m]))
        self.targetimg = pygame.image.load('images/target.png')
        transparent(self.targetimg)
        self.targetimgrect = self.targetimg.get_rect()
        self.target = Vector2(0, 0)

    def draw(self, cameraPos, windowMid, surf):
        self.cameraPos = cameraPos
        lefttop = cameraPos - windowMid
        rightbottom = cameraPos + windowMid
        lt = -(lefttop.elementwise() % 64)
        for x in range(int(lefttop.x) // 64, int(rightbottom.x) // 64 + 2):
            for y in range(int(lefttop.y) // 64, int(rightbottom.y) // 64 + 2):
                m_rect.center = vasint(lt + (Vector2(x, y) - lefttop//64) * 64)
                c = self.design.get_at((x, y))
                surf.blit(MATERIALS[(c.r, c.g, c.b)], m_rect)
        self.targetimgrect.center = vasint(self.target - cameraPos)
        surf.blit(self.targetimg, self.targetimgrect)

    def isInside(self, pos):
        return True

    def onEvent(self, event, data, mouseOn=None):
        if event == 'GlobalMouseButtonDown':
            if mouseOn == self:
                return
            self.target = Vector2(0, 0)
            return
        self.target = Vector2(data.pos) + self.cameraPos


map = Map()
characters = [map]
eventCatchers = [map]
def init(modules, **env):
    pass
start = lambda: None
stop = lambda: None
