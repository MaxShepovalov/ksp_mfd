import pygame
from pygame.locals import *
import kspButtons

moduleButtons = []
cache = {}

def init(inpcache):
	global cache
	cache = inpcache 
	moduleButtons.clear()
	numberStates = {
        "idle": {
            "button_color": (50, 50, 50),
            "text_color": (255,255,255),
            "font": kspButtons.DEFAULT_FONT,
            "size": 20
        }
    }
	kspButtons.makeButtons(moduleButtons, [cache['menu']], 0, 0, 800, 50, border = 5, states=numberStates)

def drawButtons(screen):
	kspButtons.drawButtons(screen, moduleButtons)

def processClick(xTouch, yTouch):
	btnPressed = kspButtons.findButtonByPoint(moduleButtons, xTouch, yTouch)
	if btnPressed:
		cache['moveToModule'] = btnPressed.value
		return True
	else:
		return False

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((800,480))
	init({
		'appState': "run",
		'ip': "0.0.0.0",
		'menu': ['a','b']
	})

	moduleState = "run"
	while moduleState == "run":
		screen.fill(0)
		drawButtons(screen)
		wasPressed = False
		for pyevent in pygame.event.get():
			if pyevent.type == pygame.QUIT:
				print("EVENT QUIT")
				moduleState = "exit"
			if pyevent.type == pygame.FINGERDOWN:
				# find pixel coordinate
				sx, sy = pygame.display.get_window_size()
				tx, ty = pyevent.x*sx, pyevent.y*sy
				wasPressed = processClick(tx, ty)
			if pyevent.type == pygame.MOUSEBUTTONDOWN:
				mx, my = pyevent.pos
				wasPressed = processClick(mx, my)
		if wasPressed:
			moduleState = "exit"
			break
		pygame.display.flip() #Update the screen
		pygame.time.wait(10)    
	#finish
	pygame.quit()

	print("cache: {}".format(cache))