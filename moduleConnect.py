import pygame
from pygame.locals import *
import kspButtons
import kspConnect

frames = 0
screenElements = []

def addLog(msg):
    logLines = log[0].split("\n") + [msg]
    log[0] = "\n".join(logLines[-10:])
    if logPanel:
        logPanel.value = str(log[0])

##########################################
MODULE_NAME='connect'
DISCONNECT = "disconnect"
log = [""]
kspConnect.sysSetLog(logArray=log, idx=0)
logPanel = None
setup = False
def initModule(cache):
    global setup
    global frames
    global logPanel
    states = {
        'idle': {
            "button_color": (0,0,0),
            "text_color": (255,255,255),
            "font": kspButtons.DEFAULT_FONT,
            "size": 20,
            # 'fixedWidth': 790,
            'alignV': 'bottom',
            'align': 'right'
        }
    }
    kspButtons.makeButtons(screenElements, [log], 5, 5, 790, 350, clickable=False, border = 5, states=states)
    logPanel = screenElements[0]
    addLog(MODULE_NAME+" screen\nshutdown in about 2 seconds")
    kspButtons.makeButtons(screenElements, [[DISCONNECT]], 5, 360, 790, 110, clickable=True)
    setup = True
    frames = 20
    moduleState = "run"
    return moduleState

def closeModule(cache):
    global setup
    global frames
    screenElements = []
    setup = False
    moduleState = "exit"
    frames = 0
    log[0] = ""
    return moduleState

def run(screen, moduleState, cache):
    screen.fill(0)
    global frames
    if not setup:
        raise(RuntimeError("startScreen module is not intiated"))
    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            print("EVENT QUIT")
            moduleState = "exit"
        if event.type in [pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN]:
            x, y = kspButtons.getTouchXY(event)
            btn = kspButtons.findButtonByPoint(screenElements, x, y)
            if btn and btn.value == DISCONNECT:
                print("EVENT QUIT")
                moduleState = "exit"
        if moduleState != "run":
            break
    # frames -= 1
    if not kspConnect.isConnected():
        kspConnect.connect(cache['ip'])
    else:
        cache['revertModule'] = 'start'
        cache['moveToModule'] = 'docking'
    kspButtons.drawButtons(screen, screenElements)
    if frames <= 0:
        # cache['appState'] = "exit"
        moduleState = "exit"
    return moduleState

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,480))
    cache = {
        'appState': "run",
        'ip': "0.0.0.0"
    }
    initModule(cache)
    moduleState = "run"
    while moduleState == "run":
        screen.fill(0)
        moduleState = run(screen, moduleState, cache)
        pygame.display.flip() #Update the screen
        pygame.time.wait(100)
    #finish
    closeModule(cache)
    pygame.quit()

    print("cache: {}".format(cache))