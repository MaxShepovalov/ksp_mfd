# button helper
import pygame
from enum import Enum

DEFAULT_FONT = 'unispace bd.ttf'

idleState = {
	"button_color": (150,150,150),
	"text_color": (0,0,0),
	"font": DEFAULT_FONT,
	"align": "center",
	"alightV": "center",
	'fixedWidth': False,
	"size": 60
}
pressedState = {
	"button_color": (150,255,150), # r b g
	"text_color": (0,0,0), # r g b
	"font": DEFAULT_FONT, # filename
	"align": "center", # center, left, or right
	"alignV": "center", # center, top, or bottom
	'fixedWidth': False, # False, None, or int (pixel)
	"size": 60 # int
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

def makeButtons(buttonsarr, buttonValuesTable, xPanel, yPanel, xWidth, yHeight, border=1, clickable=True, state = "idle", groups = set(), states = defaultStates):
	buttonRows = len(buttonValuesTable)
	buttonSizeY = float(yHeight)/buttonRows
	for r in range(buttonRows):
		buttonCols = len(buttonValuesTable[r])
		buttonSizeX = float(xWidth)/buttonCols
		for c in range(buttonCols):
			xCorner = xPanel+c*buttonSizeX
			yCorner = yPanel+r*buttonSizeY
			buttonsarr.append(KSPButton(
				x = xCorner+border,
				y = yCorner+border,
				w = buttonSizeX-border,
				h = buttonSizeY-border,
				value = buttonValuesTable[r][c],
				clickable = clickable,
				state = state,
				groups = groups,
				states = states)
			)

def renderText(screen, text, buttonRect, state):
	textLines = []
	totalHeight = 0
	totalWidth = 0
	bx,by,bw,bh = buttonRect
	cx = bx + .5*(bw)
	cy = by + .5*(bh)
	font = pygame.font.Font(state['font'], state['size'])
	for subtext in text.split("\n"):
		textLines.append(font.render(subtext, False, state['text_color']))
		_,_,tw,th =textLines[-1].get_rect()
		totalHeight += th
		totalWidth = max(totalWidth, tw)
	nlines = len(textLines)
	# sx, sy = pygame.display.get_window_size()
	for i in range(nlines):
		_,_,tw,th = textLines[i].get_rect()
		tx = cx - 0.5*tw # center is default
		ty = int(cy - 0.5*totalHeight + i*1.05*th) # center is default
		#vertical
		if 'alignV' in state and state['alignV'] == "top":
			ty = by + i * 1.05*th
		if 'alignV' in state and state['alignV'] == "bottom":
			ty = by + bh - (nlines-i) * 1.05*th
		#horizontal
		if 'align' in state and state['align'] == "left":
			if 'fixedWidth' in state and state['fixedWidth']:
				tw = state['fixedWidth']
			tx = max(bx, cx - .5*max(tw, totalWidth))
		elif 'align' in state and state['align'] == "right":
			tx = max(bx, bx + bw - tw)
		# ignore out of button
		if ty < by or ty > by+bh or tx > bx+bw:
			continue
		screen.blit(textLines[i], (tx, ty))

def drawButtons(screen, buttons):
	for button in buttons:
		state = button.states[button.state]
		btnRect = pygame.draw.rect(
			surface=screen, 
			color=state['button_color'],
			rect=button.rect
		)
		renderText(screen,
			buttonRect = button.rect,
			text = button.value,
			state = state
		)

def getTouchXY(pyevent):
	if pyevent.type == pygame.FINGERDOWN:
		sx, sy = pygame.display.get_window_size()
		return pyevent.x*sx, pyevent.y*sy
	if pyevent.type == pygame.MOUSEBUTTONDOWN:
		return pyevent.pos
	raise(TypeError("getTouchXY event {} is not FINGERDOWN or MOUSEBUTTONDOWN".format(pygame.event.event_name(pyevent.type))))
