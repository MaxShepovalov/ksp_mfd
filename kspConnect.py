import krpc
import math

defurl = "192.168.2.7"
c = None

logTarget = None
logIdx = None

def kspLog(msg):
    if logTarget != None and logIdx != None:
        logTarget[logIdx] = "{}\n{}".format(logTarget[logIdx],msg)
    else:
        print(str(msg))

def sysSetLog(logArray, idx):
    global logTarget
    global logIdx
    logTarget = logArray
    logIdx = idx

def connect(url):
    global c
    kspLog("connecting")
    c = krpc.connect(address=url)
    kspLog("connected")
    return c

def ls(a):
    for method in dir(a):
        if method[0] !="_":
            kspLog(method)

def res():
    if isFlight():
        av = c.space_center.active_vessel
        kspLog("Vessel: {}".format(av.name))
        for name in av.resources.names:
            kspLog(" {}: {}/{}".format(name, av.resources.amount(name), av.resources.max(name)))
    else:
        kspLog("not in flight")

def drop(conn):
    conn.close()
    kspLog("disconnected")
    exit()

def getDirection():
    if isFlight():
        av = c.space_center.active_vessel
        vessel_direction = av.rotation(av.surface_reference_frame)
        return vessel_direction
    else:
        kspLog("not in flight")
        return [0,0,0,0]

def parts():
    if isFlight():
        av = c.space_center.active_vessel
        root = av.parts.root
        stack = [(root, 1)]
        while stack:
            part, depth = stack.pop()
            kspLog("{}{}{} - {}".format('|'*(depth-1), '\\'*(depth>1), part.tag, part.title))
            for child in part.children:
                stack.append((child, depth+1))
    else:
        kspLog("not in flight")

def hint():
    if isFlight():
        av = c.space_center.active_vessel
        prevhl = None
        while True:
            for part in av.parts.all:
                if part.highlighted and prevhl != part:
                    prevhl = part
                    for module in part.modules:
                        kspLog(" m> {} {}".format(module.name, module.actions))
    else:
        kspLog("not in flight")

def getOrbit():
    if isFlight():
        av = c.space_center.active_vessel
        return av.orbit
    else:
        kspLog("not in flight")

def isFlight():
    return c.krpc.current_game_scene == c.krpc.GameScene.flight

def isConnected():
    return c != None

def vectorToAngles(vx,vy,vz):
    return (math.asin(vz)*180/math.pi, math.atan2(vx,vy)*180/math.pi)

def isTargetingVessel():
    return c.space_center.target_vessel != None or c.space_center.target_docking_port!=None

def getTargetDir():
    if not isFlight():
        return "Not in flight"
    av = c.space_center.active_vessel
    if not av:
        return "No active vesssel"
    tp = c.space_center.target_docking_port
    if not tp:
        return "Select port first"
    x,y,z = tp.direction(av.reference_frame)
    pitch, yaw = vectorToAngles(-x, -y, -z)
    ATx,ATy,ATz = tp.position(av.reference_frame)
    TAx,TAy,TAz = av.position(tp.reference_frame)
    green = ATy > 0 and TAy > 0
    ATdist = pow(ATx*ATx + ATy*ATy + ATz*ATz,0.5)
    return "TRG green: {}, pitch: {:.1f}, yaw: {:.1f}, Hshift: {:.1f}, Vshift: {:.1f}, Dist {:.1f}".format(green, pitch, yaw, ATx, ATz, ATdist)

def keepPrint():
    while True:
        try:
            print(getTargetDir())
        except KeyboardInterrupt:
            print("Stop")
            break
    print("Done")

if __name__ == "__main__":
    connect(defurl)

# get active vessel  # av = c.space_center.active_vessel
# get orbit          # orbit = av.orbit
# planet ref frame   # orbit.boy.reference_frame
# get solar panels   # sp = av.parts.solar_panels
# open solar panel   # sp[0].deployed = True
# get part direction # x,y,z = av.parts.docking_ports[2].direction(orbit.body.reference_frame)
# get pitch (rad)    # pitch = math.asin(z)
# get pitch (deg)    # pitch = math.asin(z)*180/math.pi
# get yaw (rad)      # yaw = math.atan2(x, y)
# get yaw (deg)      # yaw = math.atan2(x, y)*180/math.pi
# get vessels        # v = c.space_center.vessels
# find vessel        # rvr1 = v[17]
# set target vessel  # c.space_center.target_vessel = rvr1
# get target ports   # tdp = c.space_center.target_vessel.parts.docking_ports
# get vessel ports   # vdp = rvr1.parts.docking_ports
# set target port    # c.space_center.target_docking_port = tdp[0]
# get reltve trg dir # x,y,z = c.space_center.target_docking_port.direction(av.reference_frame)
# get flight control # f = av.flight()