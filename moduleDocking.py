import pygame
from pygame.locals import *
import kspButtons
import kspConnect
import math

screenElements = []

selectedTarget = None
selectedControl = None

def getPartList(getControl):
    av = None
    parts = []
    selectId = 0
    if getControl:
        av = kspConnect.c.space_center.active_vessel
    else:
        tp = kspConnect.c.space_center.target_docking_port
        if tp != None:
            av = tp.part.vessel
        else:
            av = kspConnect.c.space_center.target_vessel
        if not av:
            return ["no data"], 0
    print("selected vessel"+av.name)
    for p in av.parts.docking_ports:
        if p.part.tag != None and p.part.tag != '':
            print('adding tag "{}"'.format(p.part.tag))
            parts.append(p.part.tag)
        else:
            print('adding name "{}"'.format(p.part.name))
            parts.append(p.part.name)
    if getControl and selectedControl and selectedControl in parts:
        selectId = parts.index(selectedControl)
    if not getControl and selectedTarget and selectedTarget in parts:
        selectId = parts.index(selectedTarget)
    return parts, selectId

def getDockingGuidance():
    if not kspConnect.isConnected():
        return "not connected", None
    # get active vessel
    if not kspConnect.isFlight():
        return "not in flight", None
    av = kspConnect.c.space_center.active_vessel
    if not av:
        return "not in vessel", None
    # get main controlling part
    ac = av.parts.controlling
    if selectedControl and selectedControl not in [ac.tag, ac.name]:
        # get by tag
        byTag = av.parts.with_tag(selectedControl)
        if len(byTag) > 0:
            ac = byTag[0]
        else:
            byName = av.parts.with_name(selectedControl)
            if len(byName) > 0:
                ac = byName[0]
    acName = ac.tag
    if acName == None or acName == '':
        acName = ac.name
    # get target port
    tp = kspConnect.c.space_center.target_docking_port
    tpName = "not a port"
    if not tp:
        # get entire target vessel
        tp = kspConnect.c.space_center.target_vessel
        if selectedTarget:
            # get by tag
            byTag = tp.parts.with_tag(selectedTarget)
            if len(byTag) > 0:
                tp = byTag[0]
            else:
                byName = tp.parts.with_name(selectedTarget)
                if len(byName) > 0:
                    tp = byName[0]
            tpName = tp.tag
            if tpName == None or tpName == '':
                tpName = tp.name
    else:
        tp = tp.part
        if selectedTarget and selectedTarget not in [tp.name, tp.tag]:
            tv = tp.vessel
            # get by tag
            byTag = tv.parts.with_tag(selectedTarget)
            if len(byTag) > 0:
                tp = byTag[0]
            else:
                byName = tv.parts.with_name(selectedTarget)
                if len(byName) > 0:
                    tp = byName[0]
        tpName = tp.tag
        if tpName == None or tpName == '':
            tpName = tp.name
    if not tp:
        return "not targeting any vessel", None
    # get angles to target
    pitch, yaw, roll = kspConnect.getPYRRotation(ac, tp.reference_frame)
    pitch = (-pitch%360)-180 #((pitch+180+180)%360)-180
    yaw = -yaw
    roll = -roll
    # get translation to target
    # ATx,ATy,ATz = tp.position(ac.reference_frame)
    TAx,TAy,TAz = tp.position(ac.reference_frame)
    green = TAy > 0 # and ATy > 0
    ATdist = pow(TAx*TAx + TAy*TAy + TAz*TAz,0.5)
    # get relative speed
    ATvx, ATvy, ATvz = tp.velocity(ac.reference_frame)
    ATv = pow(ATvx*ATvx + ATvy*ATvy + ATvz*ATvz,0.5)
    data = {
        'targetPortName':str(tpName),
        'activeControlName':acName,
        'isGreen':green,
        'pitch':pitch, 'yaw':yaw, 'roll':roll,
        'dist':ATdist,
        'x':TAx, 'z':TAz,
        'relVX':ATvx, 'relVY':ATvy, 'relVZ':ATvz,
        'relVA':ATv
    }
    # make result
    text = "P:{:.2f} Y:{:.2f}\nR:{:.2f}\nD:{:.2f} V:{:.2f}\nX:{:.2f} Y:{:.2f} Z:{:.2f}\nVx{:.2f} y{:.2f} z{:.2f}".format(
        pitch, yaw, roll,
        ATdist, ATv,
        TAx,TAy,TAz,
        ATvx, ATvy, ATvz
    )
    return text, data

def limitValue(value, minV, maxV):
    return min(maxV, max(minV, value))

def drawGuidance(screen, guidanceData):
    middleCrossX = 600
    middleCrossY = 240
    sizeCross = 200
    if guidanceData != None:
        lineColor = (255,0,0)
        if guidanceData['isGreen']:
            lineColor = (0,255,0)
        # draw roll
        rX = math.cos(guidanceData['roll']*math.pi/180)
        rY = math.sin(guidanceData['roll']*math.pi/180)
        sizeOuter = 200
        sizeInner = 150
        pygame.draw.line(screen, (255,255,0), (middleCrossX+sizeOuter*rX,middleCrossY+sizeOuter*rY), (middleCrossX+sizeInner*rX, middleCrossY+sizeInner*rY), 3)
        # draw relative velocity
        vX = middleCrossX-sizeCross*guidanceData['relVX']/guidanceData['relVA']
        vY = middleCrossY-sizeCross*guidanceData['relVZ']/guidanceData['relVA']
        if vX > middleCrossX-sizeCross and vX < middleCrossX+sizeCross and vY > middleCrossY-sizeCross and vY < middleCrossX+sizeCross:
            if guidanceData['relVY'] < 0:
                symbolSize = 10
                pygame.draw.line(screen, lineColor, (vX-symbolSize,vY), (vX, vY-symbolSize), 3)
                pygame.draw.line(screen, lineColor, (vX,vY-symbolSize), (vX+symbolSize, vY), 3)
                pygame.draw.line(screen, lineColor, (vX+symbolSize,vY), (vX, vY+symbolSize), 3)
                pygame.draw.line(screen, lineColor, (vX,vY+symbolSize), (vX-symbolSize, vY), 3)
            else:
                pygame.draw.line(screen, lineColor, (vX-5,vY-5), (vX+5, vY+5), 3)
                pygame.draw.line(screen, lineColor, (vX-5,vY+5), (vX+5, vY-5), 3)
        # draw horizontal translation
        dX = middleCrossX+sizeCross*guidanceData['x']/10.
        dX = limitValue(dX,middleCrossX-sizeCross+20,middleCrossX+sizeCross-20)
        pygame.draw.line(screen, lineColor, (dX, middleCrossY-sizeCross), (dX, middleCrossY+sizeCross), 3)
        # draw vertical translation
        dY = middleCrossY+sizeCross*guidanceData['z']/10.
        dY = limitValue(dY,middleCrossY-sizeCross+20,middleCrossY+sizeCross-20)
        pygame.draw.line(screen, lineColor, (middleCrossX-sizeCross, dY), (middleCrossX+sizeCross, dY), 3)
        # draw target direction:
        if abs(guidanceData['pitch']) > 60 or abs(guidanceData['yaw']) > 60:
            # draw line direction
            cx = middleCrossX+sizeCross*guidanceData['yaw']/60.
            cy = middleCrossY+sizeCross*guidanceData['pitch']/60.
            pygame.draw.line(screen, (255,255,0), (middleCrossX, middleCrossY), (cx, cy), 5)
        else:
            # draw circle
            cx = middleCrossX+sizeCross*guidanceData['yaw']/60.
            cy = middleCrossY+sizeCross*guidanceData['pitch']/60.
            pygame.draw.circle(screen, (255,255,0), (cx, cy), 15, 5)
            pygame.draw.line(screen, (255,255,0), (cx,cy), (cx,cy-20), 3)
            pygame.draw.line(screen, (255,255,0), (cx-20,cy), (cx-15,cy), 3)
            pygame.draw.line(screen, (255,255,0), (cx+15,cy), (cx+20,cy), 3)
    # draw UI
    pygame.draw.line(screen, (100,100,100), (middleCrossX, middleCrossY-sizeCross), (middleCrossX, middleCrossY+sizeCross), 1)
    pygame.draw.line(screen, (100,100,100), (middleCrossX-sizeCross, middleCrossY), (middleCrossX+sizeCross, middleCrossY), 1)

##########################################
MODULE_NAME='default'
setup = False
def initModule(cache):
    global setup
    global selectedTarget
    global selectedControl
    global screenElements
    # check output of select from list
    if 'checkOutput' in cache and cache['checkOutput'] == True:
        if cache['inputType'] == 'selectTarget':
            selectedTarget = cache['inputList'][cache['inputSelect']]
        if cache['inputType'] == 'selectControl':
            selectedControl = cache['inputList'][cache['inputSelect']]
        del cache['checkOutput']
        del cache['inputList']
        del cache['inputSelect']
        del cache['inputType']
        cache['revertModule'] = 'start'
    else:
        selectedTarget = None
        selectedControl = None
    statesButton = {
        'idle': {
            "button_color": (100,100,100),
            "text_color": (255,255,255),
            "font": kspButtons.DEFAULT_FONT,
            "size": 26,
            'alignV': 'middle',
            'align': 'middle'
        }
    }
    statesData = {
        'idle': {
            "button_color": (0,0,0),
            "text_color": (255,255,255),
            "font": kspButtons.DEFAULT_FONT,
            "size": 26,
            'fixedWidth': 790,
            'alignV': 'top',
            'align': 'left'
        }
    }
    screenElements = []
    kspButtons.makeButtons(screenElements, [["control"]], 5, 5, 300, 80, clickable=True, border = 5, states=statesButton, groups={"controlSelect"})
    kspButtons.makeButtons(screenElements, [["target"]], 5, 85, 300, 80, clickable=True, border = 5, states=statesButton, groups={"targetSelect"})
    kspButtons.makeButtons(screenElements, [[MODULE_NAME+" screen"]], 5, 170, 300, 310, clickable=False, border = 5, states=statesData, groups={"exit"})
    setup = True
    moduleState = "run"
    return moduleState

def closeModule(cache):
    print("CLOSE MODULE")
    global setup
    global screenElements
    screenElements = []
    setup = False
    moduleState = "exit"
    return moduleState

def run(screen, moduleState, cache):
    screen.fill(0)
    if not setup:
        raise(RuntimeError("startScreen module is not intiated"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("EVENT QUIT")
            cache['appState'] = "exit"
        if event.type in [pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN]:
            x, y = kspButtons.getTouchXY(event)
            btn = kspButtons.findButtonByPoint(screenElements, x, y)
            if not btn:
                print("EVENT QUIT")
                moduleState = "exit"
            elif btn.inGroups({'controlSelect'}) and kspConnect.isFlight() and kspConnect.isTargetingVessel():
                #prepare possible list of control parts
                cache['inputList'], cache['inputSelect'] = getPartList(getControl=True)
                #send to module selectList
                cache['revertModule'] = 'docking'
                cache['moveToModule'] = 'selectList'
                cache['inputType'] = 'selectControl'
                moduleState = 'exit'
            elif btn.inGroups({'targetSelect'}) and kspConnect.isFlight() and kspConnect.isTargetingVessel():
                #prepare possible docking ports
                cache['inputList'], cache['inputSelect'] = getPartList(getControl=False)
                #send to module selectList
                cache['revertModule'] = 'docking'
                cache['moveToModule'] = 'selectList'
                cache['inputType'] = 'selectTarget'
                moduleState = 'exit'
        if moduleState != "run":
            break
    screenElements[2].value, rawData = getDockingGuidance()
    if rawData:
        screenElements[0].value = "CTR:"+rawData['activeControlName']
        screenElements[1].value = "TRG:"+rawData['targetPortName']
    kspButtons.drawButtons(screen, screenElements)
    drawGuidance(screen, rawData)
    return moduleState

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,480))
    cache = {
        'appState': "run",
        'ip': "0.0.0.0"
    }
    kspConnect.connect("192.168.2.7")
    initModule(cache)
    moduleState = "run"
    while moduleState == "run":
        screen.fill(0)
        moduleState = run(screen, moduleState, cache)
        pygame.display.flip() #Update the screen
        pygame.time.wait(10)
    #finish
    closeModule(cache)
    kspConnect.drop(kspConnect.c)
    pygame.quit()

    print("cache: {}".format(cache))