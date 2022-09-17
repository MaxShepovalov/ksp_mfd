import threading
import traceback

import krpc
import math
import time

krpcConnection = None
log_enabled = True
streams = []

thread = None
thread_active = True
thread_wait = 0.1
request_id = 0
request_queue = []
request_result = {}
request_agents = {}


def __ksp_log(msg):
    if log_enabled:
        tm = time.localtime()
        tm_str = "{}-{}-{}T{}:{}:{}".format(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec)
        print("{} kspConnect:{}".format(tm_str, msg))


# async buffer


def queue_stop_thread():
    queue_add_request(__stop_loop_async)


def queue_add_request(method, data=None):
    global request_id
    request_id += 1
    request_queue.append((request_id, method, data))
    __ksp_log("New request #{} for {}".format(request_id, method.__name__))
    return request_id


def queue_save_result(reference_id, data):
    if data is None:
        raise ValueError('Request #{}. Queue result cannot be None'.format(reference_id))
    request_result[reference_id] = data
    __ksp_log("Request #{} complete".format(reference_id))
    for k in range(len(request_queue)):
        queue_id, _, _ = request_queue[k]
        if queue_id == reference_id:
            del request_queue[k]
            break


def queue_get_result(reference_id):
    if reference_id in request_result:
        return request_result.pop(reference_id)
    else:
        return None


def __get_request():
    if len(request_queue) > 0:
        return request_queue[0]
    else:
        return None


def __async_loop():
    __ksp_log("Async loop started")
    while thread_active:
        task = __get_request()
        if task is not None:
            ref_id, method, data = task
            __ksp_log("Async start request #{}".format(ref_id))
            try:
                queue_save_result(ref_id, __call_method(method, data))
            except Exception as e:
                __ksp_log("Async error for request #{}\n{}".format(ref_id, traceback.format_exc()))
                queue_save_result(ref_id, e)
        else:
            time.sleep(thread_wait)
    __ksp_log("Async loop stopped")


def __call_method(method, data):
    if method is web_connect:
        result = __call_method_one_param(web_connect, data, 'kspIp', "connect expects kspIp")
    elif method is web_drop:
        result = __call_method_one_param(web_drop, data, 'conn', "drop expects conn")
    elif method is web_is_in_flight:
        result = web_is_in_flight()
    elif method is web_get_direction:
        result = web_get_direction()
    elif method is web_get_orbit:
        result = web_get_orbit()
    elif method is web_is_targeting_vessel:
        result = web_is_targeting_vessel()
    elif method is web_is_targeting_port:
        result = web_is_targeting_port()
    elif method is web_is_targeting:
        result = web_is_targeting()
    elif method is web_get_part_list:
        if data is None:
            result = web_get_part_list(filter=None)
        else:
            result = __call_method_one_param(web_get_part_list, data, 'filter', "get_part_list expects filter")
    elif method is web_get_part_filters:
        result = web_get_part_filters()
    elif method is __stop_loop_async:
        result = __stop_loop_async()
    else:
        raise KeyError('Method {} is not supported in queue'.format(method))
    return result


def __call_method_one_param(method, data, param, error_msg):
    if data is not None and param in data:
        return method(data[param])
    else:
        raise ValueError(error_msg)


def queue_agent_add_action(agent, ref_id, handler):
    if agent not in request_agents:
        request_agents[agent] = []
    request_agents[agent].append((ref_id, handler))


def queue_agent_scan_requests(memory, agent):
    if agent in request_agents:
        still_wait_requests = []
        for request_idx in range(len(request_agents[agent])):
            ref_id, handler = request_agents[agent][request_idx]
            result = queue_get_result(ref_id)
            if result is not None:
                if isinstance(result, Exception):
                    memory["log_message"] = "Error: {}".format(result)
                else:
                    handler(memory, result)
            else:
                still_wait_requests.append(request_agents[agent][request_idx])
        request_agents[agent].clear()
        request_agents[agent].extend(still_wait_requests)
        if len(request_agents[agent]) == 0:
            del request_agents[agent]

# start end connection


def start_thread():
    global thread_active
    global thread
    thread_active = True
    thread = threading.Thread(target=__async_loop)
    thread.start()


def __stop_loop_async():
    global thread_active
    thread_active = False
    return 'stopped'

def stop_thread():
    __stop_loop_async()
    if isinstance(thread, threading.Thread):
        thread.join(3)


def web_connect(ksp_ip):
    global krpcConnection
    __ksp_log("connecting")
    krpcConnection = krpc.connect(address=ksp_ip)
    __ksp_log("connected")
    return "connected"


def web_drop(conn):
    conn.close()
    __ksp_log("disconnected")
    return "disconnected"


def is_connected():
    return krpcConnection is not None


# API


def web_make_stream(value, ref_frame=None, attr=None):
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


def web_drop_streams():
    for s in streams:
        s.remove()
    streams.clear()


def web_is_in_flight():
    if krpcConnection is None:
        return ConnectionError("Not connected to KRPC")
    return krpcConnection.krpc.current_game_scene == krpcConnection.krpc.GameScene.flight


def web_get_direction():
    if web_is_in_flight():
        av = krpcConnection.space_center.active_vessel
        vessel_direction = av.rotation(av.surface_reference_frame)
        return vessel_direction
    else:
        __ksp_log("not in flight")
        return [0, 0, 0, 0]


def web_get_orbit():
    if web_is_in_flight():
        av = krpcConnection.space_center.active_vessel
        return av.orbit
    else:
        __ksp_log("not in flight")


def web_is_targeting_vessel():
    if krpcConnection is None:
        return ConnectionError("Not connected to KRPC")
    return krpcConnection.space_center.target_vessel is not None


def web_is_targeting_port():
    if krpcConnection is None:
        return ConnectionError("Not connected to KRPC")
    return krpcConnection.space_center.target_docking_port is not None


def web_is_targeting():
    return web_is_targeting_vessel() or web_is_targeting_port()


def web_get_part_list(filter=None):
    if web_is_in_flight():
        av = krpcConnection.space_center.active_vessel
        if filter is None:
            root = av.parts.root
            data = part_to_data(root, recurse=True)
            return [data], "Received data"
        elif filter in web_get_part_filters():
            view = []
            for part in eval("av.parts.{}".format(filter)):
                view.append(part_to_data(part, recurse=False))
            return view, "Received data for '{}'".format(filter)
        else:
            return None, "Invalid filter '{}'".format(filter)
    else:
        return None, "Not in flight"


def web_get_part_filters():
    filters = []
    if web_is_in_flight():
        av = krpcConnection.space_center.active_vessel
        for method in dir(av.parts):
            if method[0] != "_" and isinstance(eval("av.parts.{}".format(method)), list):
                filters.append(method)
    return filters


# math hints


def part_to_data(part, recurse=True):
    if krpcConnection is None:
        return ConnectionError("Not connected to KRPC")
    # data: {'name': 'root', 'type': 'pod', 'expanded': False, 'nodes': []}
    view_part = part
    if not isinstance(part, krpcConnection.space_center.Part) and 'part' in dir(part):
        view_part = part.part
    data = {
        'name': str(view_part.title),
        'type': str(view_part.name),
        'expanded': False,
        'part': part,
        'nodes': []
    }
    if recurse is True and len(part.children) > 0:
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
            __ksp_log("{} {}".format(type(eval("a.{}".format(method))), method))


def resources():
    if web_is_in_flight():
        av = krpcConnection.space_center.active_vessel
        __ksp_log("Vessel: {}".format(av.name))
        for name in av.resources.names:
            __ksp_log(" {}: {}/{}".format(name, av.resources.amount(name), av.resources.max(name)))
    else:
        __ksp_log("not in flight")


# def parts():
#     if web_is_in_flight():
#         av = krpcConnection.space_center.active_vessel
#         root = av.parts.root
#         stack = [(root, 1)]
#         while stack:
#             part, depth = stack.pop()
#             __ksp_log("{}{}{} - {}".format('|' * (depth - 1), '\\' * (depth > 1), part.tag, part.title))
#             for child in part.children:
#                 stack.append((child, depth + 1))
#     else:
#         __ksp_log("not in flight")


def hint():
    if web_is_in_flight():
        av = krpcConnection.space_center.active_vessel
        prevhl = None
        while True:
            for part in av.parts.all:
                if part.highlighted and prevhl != part:
                    prevhl = part
                    for module in part.modules:
                        __ksp_log(" m> {} {}".format(module.name, module.actions))
    else:
        __ksp_log("not in flight")


def get_target_dir():
    if not web_is_in_flight():
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
