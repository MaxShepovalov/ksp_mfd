import json
import os.path
import sys
import pygame
import appSelect
import moduleSettings
import moduleDevices
import kspConnect
import kspMessage
import moduleInputIP

memory = {
    "kspIp": "127.0.0.1",
    "log_enabled": True,
    "autoConnect": False,
    # ^^^ overridable ^^^ #
    # vvvv internal vvvv  #
    "kspConnected": False,
    "appState": "run",
    "version": "1.0",
    "screenX": 800,
    "screenY": 480,
    "topRowY": 50,
    "activeModule": None,
    "destroyModule": None,
    "initModule": None,
    "popup_active": False,
    "log_message": None
}
modules = {
    'appSelect': appSelect,
    'moduleSettings': moduleSettings,
    'moduleDevices': moduleDevices,
    'moduleInputIP': moduleInputIP
}
memory["initModule"] = 'appSelect'


def start(is_full_screen):
    pygame.init()
    if is_full_screen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((memory['screenX'], memory['screenY']))
    kspConnect.log_enabled = memory["log_enabled"]

    while memory['appState'] == "run":
        # check events
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                memory['appState'] = "exit"
            if event.type in [pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN]:
                x, y = get_touch_coordinates(event)
                found_app_select = appSelect.process_click(memory, x, y)
                if not found_app_select and check_module_available('activeModule'):
                    modules[memory['activeModule']].process_click(memory, x, y)

        # clear old elements first
        if check_module_available('destroyModule'):
            modules[memory['destroyModule']].destroy_module(memory)
            memory['destroyModule'] = None

        # init new elements
        if check_module_available('initModule'):
            modules[memory['initModule']].init_module(memory)
            memory['initModule'] = None

        # refresh
        appSelect.refresh(memory)
        if check_module_available('activeModule'):
            modules[memory['activeModule']].refresh(memory)
        kspMessage.refresh(memory)

        # redraw screen
        screen.fill(0)
        appSelect.draw(memory, screen)
        if check_module_available('activeModule'):
            modules[memory['activeModule']].draw(memory, screen)
        kspMessage.draw(memory, screen)

        # flip screen buffer
        pygame.display.flip()
        pygame.time.wait(100)
    # finish
    for module in modules:
        modules[module].destroy_module(memory)
    if kspConnect.is_connected():
        kspConnect.drop(kspConnect.krpcConnection)
    pygame.quit()


def get_touch_coordinates(pyevent):
    if pyevent.type == pygame.FINGERDOWN:
        sx, sy = pygame.display.get_window_size()
        return pyevent.x * sx, pyevent.y * sy
    if pyevent.type == pygame.MOUSEBUTTONDOWN:
        return pyevent.pos
    raise (TypeError(
        "getTouchXY event {} is not FINGERDOWN or MOUSEBUTTONDOWN".format(pygame.event.event_name(pyevent.type))))


def check_module_available(module_name):
    return module_name in memory and memory[module_name] is not None and \
        memory[module_name] in modules and modules[memory[module_name]] is not None


if __name__ == "__main__":
    inputArgs = [] + sys.argv
    full_screen = False
    if os.path.isfile("config.txt"):
        with open("config.txt", "r") as config_input:
            j = json.loads(config_input.read())
            if 'kspIp' in j:
                memory['kspIp'] = j["kspIp"]
            if 'autoConnect' in j:
                memory['autoConnect'] = j["autoConnect"]
            if 'log_enabled' in j:
                memory['log_enabled'] = j["log_enabled"]
    if "fullscreen" in inputArgs:
        inputArgs.remove("fullscreen")
        full_screen = True
    start(full_screen)

    with open("config.txt", "w") as config_out:
        config_out.write(json.dumps({
            "kspIp": memory["kspIp"],
            "autoConnect": memory["autoConnect"],
            "log_enabled": memory["log_enabled"]
        }))
