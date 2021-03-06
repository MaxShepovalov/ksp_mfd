import pygame
from pygame.locals import *
import moduleInputIP
import moduleStartSceen
import moduleDefault
import moduleConnect
import moduleDocking
import moduleSelectFromList
import sys

modules = {
    'start': moduleStartSceen,
    'inputIP': moduleInputIP,
    'connect': moduleConnect,
    'docking': moduleDocking,
    'selectList': moduleSelectFromList,
    'default': moduleDefault
}

#validate modules
for m in modules:
    if not modules[m].initModule:
        raise(RuntimeError("module {} doesn't have initModule(cache) method".format(m)))
    if not modules[m].closeModule:
        raise(RuntimeError("module {} doesn't have closeModule(cache) method".format(m)))
    if not modules[m].run:
        raise(RuntimeError("module {} doesn't have run(screen, appState, cache) method".format(m)))
    if not modules[m].MODULE_NAME:
        raise(RuntimeError("module {} doesn't have MODULE_NAME".format(m)))

inputArgs = []+sys.argv

activeModule = "start"
fullscreen = False
if "fullscreen" in inputArgs:
    inputArgs.remove("fullscreen")
    fullscreen = Trued

#start screen
pygame.init()
screen = None
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((800,480))

moduleState = "init"
cache = {
    'appState': "run",
    'ip': "192.168.2.7",
    "revertModule": "start"
}

try:
    while cache['appState'] == "run":
        screen.fill(0)
        if moduleState == "init":
            moduleState = modules[activeModule].initModule(cache)
        elif moduleState == "run":
            moduleState = modules[activeModule].run(screen, moduleState, cache)
        elif moduleState == "exit":
            modules[activeModule].closeModule(cache)
            if 'revertModule' in cache and cache['revertModule'] != None:
                cache['moveToModule'] = cache['revertModule']
                cache['revertModule'] = None
        if 'moveToModule' in cache and cache['moveToModule'] != None:
            activeModule = cache['moveToModule']
            cache['moveToModule'] = None
            moduleState = 'init'
        #safe exit
        if 'moveToModule' not in cache and 'revertModule' not in cache and moduleState == "exit":
            cache['appState'] = "exit"
        pygame.display.flip()
        pygame.time.wait(10)
except Exception as e:
    print(e)

pygame.quit()
print("cache: {}".format(cache))