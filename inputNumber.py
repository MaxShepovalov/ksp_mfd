#test number input
import pygame
from pygame.locals import *
pygame.init()
# DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#[7][8][9]
#[4][5][6]
#[1][2][3]
#[<][0][>]
#

BTN_BORDER = 0
BTN_VALUE = 1
BTN_WAS_PRESSED = 2
buttons = []
buttonIdleColor = (150,150,150)
buttonPressColor = (150,255,150)
def makeInputButtons(buttonsarr, x, y, xsize, ysize, btnArray):
    buttonRows = len(btnArray)
    buttonCols = len(btnArray[0])
    buttonSizeX = float(xsize)/buttonCols
    buttonSizeY = float(ysize)/buttonRows
    for r in range(buttonRows):
        for c in range(buttonCols):
            xCorner = x+c*buttonSizeX
            yCorner = y+r*buttonSizeY
            buttonsarr.append([
                (xCorner+1, yCorner+1, buttonSizeX-2, buttonSizeY-2),
                btnArray[r][c],
                False
            ])

def inRange(v, vMin, vMax):
    return v >= vMin and v < vMax

def checkClick(touchX, touchY):
    pressedButton = None
    for button in buttons+numbers:
        xMin, yMin, xW, yW = button[BTN_BORDER]
        if inRange(touchX, xMin, xMin+xW) and inRange(touchY, yMin, yMin+yW):
            if not button[BTN_WAS_PRESSED]:
                print("BTN PRESS: {} inBtns {}".format(button[BTN_VALUE], button in buttons))
                pressedButton = button
            button[BTN_WAS_PRESSED] = True
    return pressedButton

#make result
numbers = []
newNumber = True

okExit = "K"
backSpace = "<"
makeInputButtons(buttons, 500, 0, 300, 480, [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [backSpace, "0", okExit]])
makeInputButtons(numbers, 50, 30, 400, 60, [["0", "0", "0", "0"]])

screen = pygame.display.set_mode((800,480))
buttonFont = pygame.font.Font('unispace bd.ttf', 60)
numberFont = pygame.font.Font('unispace bd.ttf', 40)
pyloop = True
while pyloop:
    screen.fill(0)
    btnPressed = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("EVENT QUIT")
            pyloop = False
        if event.type == pygame.FINGERDOWN:
            sx, sy = pygame.display.get_window_size()
            tx, ty = event.x*sx, event.y*sy
            #print("EVENT FINGERDOWN {} {}".format(tx, ty))
            btnPressed = checkClick(tx, ty)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            #print("EVENT MOUSEBUTTONDOWN {} {}".format(mx, my))
            btnPressed = checkClick(mx, my)
        if event.type in [pygame.FINGERUP, pygame.MOUSEBUTTONUP]:
            for button in buttons:
                button[BTN_WAS_PRESSED] = False
    #process buttons
    if btnPressed in numbers:
        newNumber = True
        for number in numbers:
            number[BTN_WAS_PRESSED] = number == btnPressed
    if btnPressed in buttons:
        if btnPressed[BTN_VALUE] == okExit:
            pyloop = False
            break
        for number in numbers:
            if number[BTN_WAS_PRESSED]:
                if btnPressed[BTN_VALUE] == backSpace:
                    number[BTN_VALUE] = number[BTN_VALUE][:-1]
                    if number[BTN_VALUE] == "":
                        number[BTN_VALUE] = "0"
                elif newNumber:
                    newNumber = False
                    number[BTN_VALUE] = btnPressed[BTN_VALUE]
                else:
                    number[BTN_VALUE] = (number[BTN_VALUE]+btnPressed[BTN_VALUE])[-3:]
    # draw buttons
    for button in buttons:
        x,y,rx,ry=button[BTN_BORDER]
        color = buttonIdleColor
        if button[BTN_WAS_PRESSED]:
            color = buttonPressColor
        btnRect = pygame.draw.rect(
            surface=screen, 
            color=color,
            rect=(x, y, rx, ry)
        )
        textsurface = buttonFont.render(button[BTN_VALUE], False, (0,0,0))
        screen.blit(textsurface, (x+0.3*rx, y+0.3*ry))

    # draw numbers
    for number in numbers:
        x,y,rx,ry=number[BTN_BORDER]
        color = buttonIdleColor
        if number[BTN_WAS_PRESSED]:
            color = buttonPressColor
        btnRect = pygame.draw.rect(
            surface=screen, 
            color=color,
            rect=(x, y, rx, ry)
        )
        textsurface = numberFont.render(number[BTN_VALUE], False, (0,0,0))
        screen.blit(textsurface, (x+0.1*rx, y+0.1*ry))
    # pygame.display.update()
    pygame.display.flip() #Update the screen
    pygame.time.wait(10)
pygame.quit()
ip = ""
for number in numbers:
    ip += number[BTN_VALUE]+"."
print("IP "+ip[:-1])