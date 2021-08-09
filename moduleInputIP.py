#test number input
import pygame
from pygame.locals import *
import kspButtons
# DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#[7][8][9]
#[4][5][6]
#[1][2][3]
#[<][0][>]

#constants
OK_EXIT = "K"
BACKSPACE = "<"

MODULE_NAME = "inputIP"


buttons = []
numbers = []
setup=False

def prepareButtons(buttons, numbers, cache):
	if not setup:
		raise(RuntimeError(MODULE_NAME+" module is not intiated"))
	#make buttons
	#makeButtons(buttonsarr, buttonValuesTable, xPanel, yPanel, xWidth, yHeight, state = "idle", groups = set(), states = defaultStates)
	buttonValues = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [BACKSPACE, "0", OK_EXIT]]
	kspButtons.makeButtons(buttons, buttonValues, 500, 0, 300, 480, groups = set("buttons"))

	numberValues = [["0", "0", "0", "0"]]
	if 'ip' in cache and cache['ip'].count('.') == 3:
		numberValues = [cache['ip'].split(".")]
	numberStates = {
		"idle": {
			"button_color": (50, 50, 50),
			"text_color": (155,155,155),
			"font": kspButtons.DEFAULT_FONT,
			"size": 40
		},
		"pressed": {
			"button_color": (50, 50, 50),
			"text_color": (0,255,0),
			"font": kspButtons.DEFAULT_FONT,
			"size": 40  
		}
	}
	kspButtons.makeButtons(numbers, numberValues, 50, 30, 400, 60, state="idle", groups = set("numbers"), states=numberStates)

def processClick(xTouch, yTouch, moduleState):
	if not setup:
		raise(RuntimeError("inputNumber module is not intiated"))
	btnPressed = kspButtons.findButtonByPoint(buttons+numbers, xTouch, yTouch)
	#process buttons
	if btnPressed in numbers:
		kspButtons.untouchAllButtons(numbers)
		btnPressed.state = "pressed"
	if btnPressed in buttons and btnPressed.state == btnPressed.idlestate:
		btnPressed.state = "pressed"
		if btnPressed.value == OK_EXIT:
			moduleState = "exit"
		else:
			# search pressed number
			number = kspButtons.findButtonInState(numbers, "pressed")
			if number:
				if btnPressed.value == BACKSPACE:
					number.value = str(int(float(number.value)/10))
				else:
					number.value = str(int(number.value)*10+int(btnPressed.value))[-3:]
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
		moduleState = processClick(tx, ty, moduleState)
	if pyevent.type == pygame.MOUSEBUTTONDOWN:
		mx, my = pyevent.pos
		moduleState = processClick(mx, my, moduleState)
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

	#print IP result
	ip = ""
	for number in numbers:
		ip += number.value+"."
	cache['ip'] = ip[:-1]

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
		'ip': "0.0.0.0"
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