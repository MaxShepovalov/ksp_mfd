import pygame
from pygame.locals import *
import kspButtons
import kspCache

MODULE_NAME = "startScreen"
setup = False
buttons = []
CONNECT = "Connect"
EXIT = "Exit"

def processClick(xTouch, yTouch, moduleState):
	if not setup:
		raise(RuntimeError("inputNumber module is not intiated"))
	btnPressed = kspButtons.findButtonByPoint(buttons, xTouch, yTouch)
	if btnPressed and btnPressed.value == CONNECT:
		pass
	if btnPressed in buttons and btnPressed.state == btnPressed.idlestate:
		if btnPressed.value == EXIT:
			moduleState = 'exit'
		elif btnPressed.value == CONNECT:
			# activate next module
			moduleState = 'connect'
		else:
			# change ip
			moduleState = 'inputIP'
	return moduleState

def doEvent(pyevent, moduleState):
	if not setup:
		raise(RuntimeError("startScreen module is not intiated"))
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

##########################################
def initModule(cache):
	global buttons
	global setup
	buttons = []
	setup = True
	#info screen
	buttonValue = [["IP: {}".format(cache['ip'])], [CONNECT, EXIT]]
	kspButtons.makeButtons(buttons, buttonValue, 5, 5, 790, 470, border = 5)
	return "run"

def closeModule(cache):
	global buttons
	global setup
	buttons = []
	setup = False
	return "exit"

def run(screen, moduleState, cache):
	screen.fill(0)
	if not setup:
		raise(RuntimeError("startScreen module is not intiated"))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print("EVENT QUIT")
			moduleState = "exit"
		else:
			moduleState = doEvent(event, moduleState)
		if moduleState != "run":
			break
	kspButtons.drawButtons(screen, buttons)
	if moduleState == "exit":
		cache['appState'] = "exit"
	if moduleState not in ['init', 'run', 'exit']:
		cache['revertModule'] = 'start'
		cache['moveToModule'] = moduleState
	return moduleState

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((800,480))
	cache = kspCache.getDefaultCache()
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