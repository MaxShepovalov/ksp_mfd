#test number input
import pygame
from pygame.locals import *
import kspButtons

#[  up  ]
#[ down ]
#[select]

MODULE_NAME = "inputSelectList"


buttons = []
#list to select from
numbers = []
setup=False

def getSublist(alist, center, size):
    mn = max(0, center - int((size-1)/2))
    mx = min(len(alist), center + int((size+1)/2))
    if mn == 0:
        mx = min(len(alist), size)
    elif mx == len(alist):
        mn = max(0, len(alist)-size)
    return alist[mn:mx], center-mn

def reassignList(cache):
    subValues, listSelect = getSublist(cache['inputList'], cache['inputSelect'], 9)
    if len(numbers) != len(subValues):
        raise IndexError("Sizes are not matching numbers:{} values:{}".format(len(numbers), len(subValues)))
    for i in range(len(numbers)):
        numbers[i].value = subValues[i]
    numbers[listSelect].state = "selected"

def prepareButtons(buttons, numbers, cache):
    if not setup:
        raise(RuntimeError(MODULE_NAME+" module is not intiated"))
    #make buttons
    #makeButtons(buttonsarr, buttonValuesTable, xPanel, yPanel, xWidth, yHeight, state = "idle", groups = set(), states = defaultStates)
    buttonValues = [["up"], ["down"], ["select"]]
    kspButtons.makeButtons(buttons, buttonValues, 5, 5, 290, 480, groups = set("buttons"))
    # make strings for list
    numberValues = []
    for i in range(min(9, len(cache['inputList']))):
        numberValues.append(["value"])
    numberStates = {
        "idle": {
            "button_color": (0, 0, 0),
            "text_color": (155,155,155),
            "font": kspButtons.DEFAULT_FONT,
            "size": 40
        },
        "selected": {
            "button_color": (0, 0, 0),
            "text_color": (255,255,0),
            "font": kspButtons.DEFAULT_FONT,
            "size": 40  
        }
    }
    kspButtons.makeButtons(numbers, numberValues, 300, 5, 500, 480, state="idle", groups = set("numbers"), states=numberStates)
    reassignList(cache)

def processClick(xTouch, yTouch, moduleState, cache):
    if not setup:
        raise(RuntimeError("inputNumber module is not intiated"))
    btnPressed = kspButtons.findButtonByPoint(buttons+numbers, xTouch, yTouch)
    #process buttons
    if btnPressed in buttons:
        btnPressed.state = "pressed"
        kspButtons.untouchAllButtons(numbers)
        if btnPressed.value == 'select':
            moduleState = "exit"
            cache['checkOutput'] = True
        elif btnPressed.value == 'up':
            cache['inputSelect'] = max(0, cache['inputSelect']-1)
            reassignList(cache)
        elif btnPressed.value == 'down':
            cache['inputSelect'] = min(len(cache['inputList'])-1, cache['inputSelect']+1)
            reassignList(cache)
    return moduleState



##########################################3
def doEvent(pyevent, moduleState, cache):
    if not setup:
        raise(RuntimeError("inputNumber module is not intiated"))
    if pyevent.type == pygame.QUIT:
        print("EVENT QUIT")
        cache['appState'] = "exit"
    if pyevent.type == pygame.FINGERDOWN:
        # find pixel coordinate
        sx, sy = pygame.display.get_window_size()
        tx, ty = pyevent.x*sx, pyevent.y*sy
        moduleState = processClick(tx, ty, moduleState, cache)
    if pyevent.type == pygame.MOUSEBUTTONDOWN:
        mx, my = pyevent.pos
        moduleState = processClick(mx, my, moduleState, cache)
    if pyevent.type in [pygame.FINGERUP, pygame.MOUSEBUTTONUP]:
        kspButtons.untouchAllButtons(buttons)
    return moduleState

def initModule(cache):
    global buttons
    global numbers
    global setup
    buttons = []
    numbers = []
    setup = True
    prepareButtons(buttons, numbers, cache)
    return "run"

def closeModule(cache):
    global buttons
    global numbers
    global setup

    buttons = []
    numbers = []
    setup = False
    return "exit"

def run(screen, moduleState, cache):
    screen.fill(0)
    if not setup:
        raise(RuntimeError("inputNumber module is not intiated"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("EVENT QUIT")
            moduleState = "exit"
        else:
            moduleState = doEvent(event, moduleState, cache)
        if moduleState == "exit":
            break
    kspButtons.drawButtons(screen, buttons+numbers)
    return moduleState

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,480))
    cache = {
        'appState': "run",
        'ip': "0.0.0.0",
        'inputList':["example1","example2","example3","example4","example5","example6","example7","example8","example9","example10","example11","example12"],
        'inputSelect': 7
    }
    initModule(cache)
    moduleState = "run"
    while moduleState == "run":
        screen.fill(0)
        moduleState = run(screen, moduleState, cache)
        pygame.display.flip() #Update the screen
        pygame.time.wait(10)    
    #finish
    closeModule(cache)
    pygame.quit()

    print("cache: {}".format(cache))