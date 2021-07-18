import pygame
from pygame.locals import *
import kspButtons

frames = 0
text = []

##########################################
MODULE_NAME='default'
setup = False
def initModule(cache):
	global setup
	global frames
	kspButtons.makeButtons(text, [[MODULE_NAME+" screen"],["shutdown in 2 seconds"]], 5, 5, 790, 470, clickable=False, border = 5)
	setup = True
	frames = 500
	moduleState = "run"
	return moduleState

def closeModule(cache):
	global setup
	global frames
	text = []
	setup = False
	moduleState = "exit"
	frames = 0
	return moduleState

def run(screen, moduleState, cache):
	global frames
	if not setup:
		raise(RuntimeError("startScreen module is not intiated"))
	for event in pygame.event.get():
		if event.type in [pygame.QUIT, pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN]:
			print("EVENT QUIT")
			moduleState = "exit"
		if moduleState != "run":
			break
	frames -= 1
	kspButtons.drawButtons(screen, text)
	if frames <= 0:
		cache['appState'] = "exit"
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
		pygame.time.wait(10)
	#finish
	closeModule(cache)
	pygame.quit()

	print("cache: {}".format(cache))