import pygame
import appSelect
import moduleSettings
import moduleDevices
import kspConnect

memory = {
    "kspIp": "127.0.0.1",
    "log_enabled": True,
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
    "popup_active": False
}
modules = {
    'appSelect': appSelect,
    'moduleSettings': moduleSettings,
    'moduleDevices': moduleDevices
}
memory["initModule"] = 'appSelect'


def start():
    pygame.init()
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
        if check_module_available('activeModule'):
            modules[memory['activeModule']].refresh(memory)

        # redraw screen
        screen.fill(0)
        appSelect.draw(memory, screen)
        if check_module_available('activeModule'):
            modules[memory['activeModule']].draw(memory, screen)

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
    start()
