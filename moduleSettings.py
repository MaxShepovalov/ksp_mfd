import kspButtons
import kspConnect

buttons_array = []
created = False
connect_status_message = {
    True: "Connected",
    False: "Disconnected"
}


def init_module(memory):
    global created
    buttons_array.clear()
    kspButtons.make_buttons(buttons_array,
                            [[memory['kspIp']], ["connect"], [connect_status_message[memory['kspConnected']]], ["exit"]],
                            x=0, y=memory["topRowY"]+5,
                            w=memory["screenX"], h=memory["screenY"]-2*memory["topRowY"]-10,
                            button_specials=[["ip"], ["connect"], ["statusMessage"], ["exit"]]
    )
    not_a_button = kspButtons.find_button_by_special(buttons_array, "statusMessage")
    not_a_button.clickable = False
    not_a_button.styles[kspButtons.IDLE_STYLE] = {
        "button_color": kspButtons.BLACK,
        "text_color": kspButtons.WHITE,
        "font": kspButtons.DEFAULT_FONT,
        "align": "center",
        "alightV": "center",
        'fixedWidth': False,
        "size": 60
    }
    created = True


def draw(memory, screen):
    status_text = kspButtons.find_button_by_special(buttons_array, "statusMessage")
    status_text.value = connect_status_message[memory['kspConnected']]
    kspButtons.draw(screen, buttons_array)
    # don't hold pressed style
    kspButtons.reset_all_buttons(buttons_array)


def process_click(memory, x, y):
    if not memory["popup_active"]:
        pressed_button = kspButtons.find_button_by_point(buttons_array, x, y)
        if pressed_button is not None:
            pressed_button.set_style(kspButtons.PRESSED_STYLE)
            if pressed_button.special == "exit":
                memory['appState'] = "exit"
            elif pressed_button.special == "ip":
                memory['destroyModule'] = 'moduleSettings'
                memory['activeModule'] = 'moduleInputIP'
                memory['initModule'] = 'moduleInputIP'
            elif pressed_button.special == "connect":
                memory["log_message"] = "Connecting to {}".format(memory['kspIp'])
                if kspConnect.is_connected():
                    kspConnect.queue_agent_add_action(
                        'moduleSettings',
                        kspConnect.queue_add_request(kspConnect.web_drop, {'conn': kspConnect.krpcConnection}),
                        handler_connection_lost)
                kspConnect.queue_agent_add_action(
                    'moduleSettings',
                    kspConnect.queue_add_request(kspConnect.web_connect, {'kspIp': memory['kspIp']}),
                    handler_connection_acquired)
            return True
    return False


def handler_connection_lost(memory, result):
    memory["kspConnected"] = False
    memory["log_message"] = "Disconnected"
    not_a_button = kspButtons.find_button_by_special(buttons_array, "statusMessage")
    if not_a_button is not None:
        not_a_button.value = connect_status_message[memory['kspConnected']]


def handler_connection_acquired(memory, result):
    memory["kspConnected"] = True
    memory["log_message"] = "Connected"
    not_a_button = kspButtons.find_button_by_special(buttons_array, "statusMessage")
    if not_a_button is not None:
        not_a_button.value = connect_status_message[memory['kspConnected']]


def refresh(memory):
    kspConnect.queue_agent_scan_requests(memory, 'moduleSettings')


def destroy_module(memory):
    global created
    created = False
    buttons_array.clear()
