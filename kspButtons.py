# button helper
import pygame
from enum import Enum

DEFAULT_FONT = 'unispace bd.ttf'

idleState = {
	"button_color": (150,150,150),
	"text_color": (0,0,0),
	"font": DEFAULT_FONT,
	"size": 60
}
pressedState = {
	"button_color": (150,255,150),
	"text_color": (0,0,0),
	"font": DEFAULT_FONT,
	"size": 60
}

defaultStates = {"idle":idleState, "pressed":pressedState}

class KSPButton:
	def __init__(self, x, y, w, h, value, clickable=True, state="idle", groups = set(), states = defaultStates):
		self.rect = (x, y, w, h)
		self.value = str(value)
		self.state = str(state)
		self.idlestate = str(state)
		self.states = {**states}
		self.groups = groups
		self.clickable = clickable
		for stateId in self.states:
			btnstate = self.states[stateId]
			if 'button_color' not in btnstate:
				raise(KeyError("button \"{}\" state \"{}\" button_color is null".format(value, stateId)))
			if 'text_color' not in btnstate:
				raise(KeyError("button \"{}\" state \"{}\" text_color is null".format(value, stateId)))
			if 'font' not in btnstate:
				raise(KeyError("button \"{}\" state \"{}\" font is null".format(value, stateId)))
			if 'size' not in btnstate:
				raise(KeyError("button \"{}\" state \"{}\" size is null".format(value, stateId)))
		if self.state not in self.states:
			raise(ValueError("buttton \"{}\" default state {} is not set".format(value, self.state)))

	def addState(self, stateid, state):
		self.states[stateid] = state

	def addStates(self, states):
		self.states = {**self.states, **states}

	def isPressed(self, xTouch, yTouch):
		x, y, w, h = self.rect
		return self.clickable and xTouch>=x  and xTouch<(x+w) and yTouch>=y and yTouch<(y+h)

	def inGroups(self, groups = set()):
		return len(groups.difference(self.groups)) == 0

# find button in list by touch
def findButtonByPoint(buttons, x, y, groups = set()):
	for button in buttons:
		if button.isPressed(x, y) and button.inGroups(groups):
			return button

def untouchAllButtons(buttons, groups = set()):
	for button in buttons:
		if button.inGroups(groups):
			button.state = str(button.idlestate)

def findButtonInState(buttons, state, groups = set()):
	for button in buttons:
		if button.state == state and button.inGroups(groups):
			return button

def makeButtons(buttonsarr, buttonValuesTable, xPanel, yPanel, xWidth, yHeight, border=1, state = "idle", groups = set(), states = defaultStates):
	buttonRows = len(buttonValuesTable)
	buttonSizeY = float(yHeight)/buttonRows
	for r in range(buttonRows):
		buttonCols = len(buttonValuesTable[r])
		buttonSizeX = float(xWidth)/buttonCols
		for c in range(buttonCols):
			xCorner = xPanel+c*buttonSizeX
			yCorner = yPanel+r*buttonSizeY
			buttonsarr.append(KSPButton(
				xCorner+border, yCorner+border, buttonSizeX-border, buttonSizeY-border,
				buttonValuesTable[r][c],
				state = state,
				groups = groups,
				states = states)
			)

def drawButtons(screen, buttons):
	for button in buttons:
		state = button.states[button.state]
		btnRect = pygame.draw.rect(
			surface=screen, 
			color=state['button_color'],
			rect=button.rect
		)
		textFont = pygame.font.Font(state['font'], state['size'])
		textsurface = textFont.render(button.value, False, state['text_color'])
		x,y,w,h = button.rect
		_,_,tw,th =textsurface.get_rect()
		tx = x + .5*(w-tw)
		ty = y + .5*(h-th)
		screen.blit(textsurface, (tx, ty))