#!/usr/bin/python3
# encoding=utf-8

'''
内核

每个模块都应提供：
    init : function(modules : list of module, **env : dict of (str, *)) -> NoneType
        env的内容：side为'c'或's'，指明客户端或服务器端；调用stop会结束程序；setjob设置内核启动后要进行的任务；
    start : function() -> NoneType
        应当立即返回
    stop : function() -> NoneType
'''

from sys import argv, stderr
from time import sleep
import importlib

def printUsage():
    print('usage: %s client|server [modules...]' % argv[0], file=stderr)

if len(argv) < 2:
    printUsage()
    exit()

if 'client'.startswith(argv[1].lower()):
    SIDE = 'c'
elif 'server'.startswith(argv[1].lower()):
    SIDE = 's'
else:
    printUsage()
    exit()

def job():
    pass
def setjob(f):
    global job
    job = f

modules = list(map(importlib.import_module, argv[2:]))
def stop():
    for module in modules:
        module.stop()
for module in modules:
    module.init(modules, side=SIDE, stop=stop, setjob=setjob)
for module in modules:
    module.start()
job()
