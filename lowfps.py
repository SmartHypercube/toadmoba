# encoding=utf-8


'''
将帧率控制在8以内
'''


def init(modules, **env):
    for module in modules:
        module.FPS = 8
        module.SPF = 1 / 8
def start():
    pass
def stop():
    pass
