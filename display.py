# encoding=utf-8


'''
显示游戏界面

包含要绘制的图形的模块，应提供：
    characters : list of <Thing>

<Thing>应提供：
    order : int
    draw : function(cameraPos : tuple of int, windowMid : tuple of int, surf : Surface) -> NoneType

控制镜头的模块，应提供：
    camera : <Camera>

<Camera>应提供：
    position : tuple of int

欲接收事件的模块，应提供：
    eventCatchers : list of <EventCatcher>

<EventCatcher>应提供：
    order : int
    events : list of str
        支持的事件类型：MouseEnter, MouseLeave, MouseButtonDown, MouseButtonUp, KeyDown, KeyUp
        试验支持的事件类型：VideoExpose, VideoResize, ActiveEvent, Quit
        任何一个鼠标事件都可以通过前缀Global-来选择接收所有元素上的此类事件
        否则只发送给焦点元素
    isInside : function(pos : tuple of int) -> bool
    onEvent : function(event : str, data : *, mouseOn=None : <EventCatcher>) -> bool
'''


import time, threading
from time import sleep

import pygame
from pygame.locals import *


def inthread(f):
    '''使函数在独立线程中运行的装饰器'''
    return threading.Thread(target=f).start

class _:
    events = []
    order = 1000
BLANK = _()
WINDOWSIZE = (1280, 720)
windowMid = (WINDOWSIZE[0] // 2, WINDOWSIZE[1] // 2)
FPS = 60
EVENT_TABLE = {
        MOUSEMOTION: 'MouseMotion',
        MOUSEBUTTONDOWN: 'MouseButtonDown',
        MOUSEBUTTONUP: 'MouseButtonUp',
        KEYDOWN: 'KeyDown',
        KEYUP: 'KeyUp',
        VIDEOEXPOSE: 'VideoExpose',
        VIDEORESIZE: 'VideoResize',
        ACTIVEEVENT: 'ActiveEvent',
        QUIT: 'Quit'
}

class Display:

    def __init__(self):
        pygame.init()
        self.displaySurf = pygame.display.set_mode(WINDOWSIZE, FULLSCREEN, 32)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('League of Toads')
        self.characters = []
        class _: position = (0, 0)
        self.camera = _()
        self.eventCatchers = []
        self.running = False

    def init(self, modules, **env):
        # 收集所有要绘制的图形
        for module in modules:
            try: self.characters.extend(module.characters)
            except: pass
            try: self.camera = module.camera
            except: pass
            try: self.eventCatchers.extend(module.eventCatchers)
            except: pass
        self.characters.sort(key=lambda c: c.order, reverse=True)
        self.eventCatchers.sort(key=lambda e: e.order)
        self.running = True
        self.envstop = env['stop']
        def job(c=self.clock, display=self):
            while display.running:
                pygame.event.pump()
            pygame.quit()
        env['setjob'](job)

    def start(self):
        mouseOn = BLANK
        while self.running:
            cameraPos = self.camera.position
            for character in self.characters:
                character.draw(cameraPos, windowMid, self.displaySurf)
            for data in pygame.event.get():
                event = EVENT_TABLE.get(data.type, '')
                if event == 'Quit':
                    envstop()
                elif event.startswith('Mouse'):
                    if mouseOn.order >= 100 or not mouseOn.isInside(data.pos):
                        if 'MouseLeave' in mouseOn.events:
                            mouseOn.onEvent('MouseLeave', data.pos)
                        mouseOn = BLANK
                        for eventCatcher in self.eventCatchers:
                            if eventCatcher.isInside(data.pos):
                                mouseOn = eventCatcher
                                if 'MouseEnter' in mouseOn.events:
                                    mouseOn.onEvent('MouseEnter', data.pos)
                                break
                    if event != 'MouseMotion':
                        if event in mouseOn.events:
                            mouseOn.onEvent(event, data)
                        event = 'Global' + event
                        for eventCatcher in self.eventCatchers:
                            if event in eventCatcher.events:
                                eventCatcher.onEvent(event, data, mouseOn)
                elif event.startswith('Key'):
                    for eventCatcher in self.eventCatchers:
                        if event in eventCatcher.events:
                            if eventCatcher.onEvent(event, data):
                                break
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def stop(self):
        self.running = False


display = Display()
init = display.init
@inthread
def start():
    display.start()
stop = display.stop
