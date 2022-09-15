import krpc
import math

krpcConnection = None
log_enabled = True
streams = []


def ksp_log(msg):
    if log_enabled:
        print(msg)


# start end connection


def connect(ksp_ip):
    global krpcConnection
    ksp_log("connecting")
    krpcConnection = krpc.connect(address=ksp_ip)
    ksp_log("connected")
    return krpcConnection


def drop(conn):
    conn.close()
    ksp_log("disconnected")


def is_connected():
    return krpcConnection is not None


# API


def make_stream(value, ref_frame=None, attr=None):
    stream = None
    if ref_frame is None:
        if attr is None:
            stream = krpcConnection.add_stream(value)
        else:
            stream = krpcConnection.add_stream(value, attr)
    else:
        stream = krpcConnection.add_stream(value, ref_frame)
    if stream is not None:
        streams.append(stream)
    return stream


def drop_streams():
    for s in streams:
        s.remove()
    streams.clear()


def is_in_flight():
    return krpcConnection.krpc.current_game_scene == krpcConnection.krpc.GameScene.flight


def get_direction():
    if is_in_flight():
        av = krpcConnection.space_center.active_vessel
        vessel_direction = av.rotation(av.surface_reference_frame)
        return vessel_direction
    else:
        ksp_log("not in flight")
        return [0, 0, 0, 0]


def get_orbit():
    if is_in_flight():
        av = krpcConnection.space_center.active_vessel
        return av.orbit
    else:
        ksp_log("not in flight")


def is_targeting_vessel():
    return krpcConnection.space_center.target_vessel is not None


def is_targeting_port():
    return krpcConnection.space_center.target_docking_port is not None


def is_targeting():
    return is_targeting_vessel() or is_targeting_port()


def get_part_list():
    # {'name': 'root', 'type': 'pod', 'expanded': False, 'nodes': []}
    if is_in_flight():
        av = krpcConnection.space_center.active_vessel
        root = av.parts.root
        data = part_to_data(root)
        return data, "Received data"
    else:
        return None, "Not in flight"


# math hints


def part_to_data(part):
    data = {
        'name': str(part.title),
        'type': str(part.name),
        'expanded': False,
        'part': part,
        'nodes': []
    }
    if len(part.children) > 0:
        for connected in part.children:
            data['nodes'].append(part_to_data(connected))
    return data


def vector_to_angles(vx, vy, vz):
    return math.asin(vz) * 180 / math.pi, math.atan2(vx, vy) * 180 / math.pi


def get_pyr_rotation(obj, ref_frame):
    qx, qy, qz, qw = obj.rotation(ref_frame)
    roll = math.atan2(2 * qy * qw - 2 * qx * qz, 1 - 2 * qy * qy - 2 * qz * qz)
    pitch = math.atan2(2 * qx * qw - 2 * qy * qz, 1 - 2 * qx * qx - 2 * qz * qz)
    yaw = math.asin(2 * qx * qy + 2 * qz * qw)
    return pitch * 180 / math.pi, yaw * 180 / math.pi, roll * 180 / math.pi


# manual tests


def ls(a):
    for method in dir(a):
        if method[0] != "_":
            ksp_log(method)


def resources():
    if is_in_flight():
        av = krpcConnection.space_center.active_vessel
        ksp_log("Vessel: {}".format(av.name))
        for name in av.resources.names:
            ksp_log(" {}: {}/{}".format(name, av.resources.amount(name), av.resources.max(name)))
    else:
        ksp_log("not in flight")


def parts():
    if is_in_flight():
        av = krpcConnection.space_center.active_vessel
        root = av.parts.root
        stack = [(root, 1)]
        while stack:
            part, depth = stack.pop()
            ksp_log("{}{}{} - {}".format('|' * (depth - 1), '\\' * (depth > 1), part.tag, part.title))
            for child in part.children:
                stack.append((child, depth + 1))
    else:
        ksp_log("not in flight")


def hint():
    if is_in_flight():
        av = krpcConnection.space_center.active_vessel
        prevhl = None
        while True:
            for part in av.parts.all:
                if part.highlighted and prevhl != part:
                    prevhl = part
                    for module in part.modules:
                        ksp_log(" m> {} {}".format(module.name, module.actions))
    else:
        ksp_log("not in flight")


def get_target_dir():
    if not is_in_flight():
        return "Not in flight"
    av = krpcConnection.space_center.active_vessel
    if not av:
        return "No active vessel"
    tp = krpcConnection.space_center.target_docking_port
    if not tp:
        return "Select port first"
    x, y, z = tp.direction(av.reference_frame)
    pitch, yaw = vector_to_angles(-x, -y, -z)
    at_x, at_y, at_z = tp.position(av.reference_frame)
    ta_x, ta_y, ta_z = av.position(tp.reference_frame)
    green = at_y > 0 and ta_y > 0
    at_distance = pow(at_x * at_x + at_y * at_y + at_z * at_z, 0.5)
    return "TRG green: {}, pitch: {:.1f}, yaw: {:.1f}, Hshift: {:.1f}, Vshift: {:.1f}, Dist {:.1f}".format(
        green, pitch, yaw, at_x, at_distance, at_distance)


def keep_print():
    while True:
        try:
            print(get_target_dir())
        except KeyboardInterrupt:
            print("Stop")
            break
    print("Done")

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
