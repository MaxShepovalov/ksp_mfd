import kspButtons

elements = []
setup = False
just_selected = False


def init_module(memory):
    elements.clear()
    button_values = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["<", "0", "ok"]]
    initial_number_values = [memory['kspIp'].split('.')]
    ip_specials = [[0, 1, 2, 3]]
    kspButtons.make_buttons(elements, button_values=button_values, x=memory['screenX'] * 0.6, y=memory['topRowY'],
                            w=memory['screenX'] * 0.4, h=memory["screenY"] - 2 * memory["topRowY"] - 10, border=10,
                            groups={'buttons'})
    elements[-1].groups = {'buttons', 'ok'}
    elements[-3].groups = {'buttons', 'backspace'}
    kspButtons.make_buttons(elements, button_values=initial_number_values, x=0, y=memory['topRowY'],
                            w=memory['screenX'] * 0.5, h=60, border=5, groups={'numbers'},
                            button_specials=ip_specials, styles={
            kspButtons.IDLE_STYLE: {
                "button_color": kspButtons.GREY,
                "text_color": kspButtons.WHITE,
                "font": kspButtons.DEFAULT_FONT,
                "size": 40
            },
            kspButtons.PRESSED_STYLE: {
                "button_color": kspButtons.GREEN,
                "text_color": kspButtons.BLACK,
                "font": kspButtons.DEFAULT_FONT,
                "size": 40
            }
        })
    memory['log_message'] = "Enter IP address of KRPC"


def draw(memory, screen):
    kspButtons.draw(screen, elements)
    kspButtons.reset_all_buttons(elements, groups={'buttons'})


def process_click(memory, x, y):
    global just_selected
    pressed_button = kspButtons.find_button_by_point(elements, x, y)
    if pressed_button is not None and pressed_button.in_groups({'ok'}):
        pressed_button.set_style(kspButtons.PRESSED_STYLE)
        numbers = kspButtons.find_all_by_groups(elements, {'numbers'})
        new_ip = [0, 0, 0, 0]
        for number in numbers:
            new_ip[number.special] = number.value
        memory['kspIp'] = '.'.join(new_ip)
        memory['log_message'] = "IP is now {}".format(memory['kspIp'])
        memory['destroyModule'] = 'moduleInputIP'
        memory['activeModule'] = 'moduleSettings'
        memory['initModule'] = 'moduleSettings'
    elif pressed_button is not None and pressed_button.in_groups({'buttons'}):
        pressed_button.set_style(kspButtons.PRESSED_STYLE)
        selected_number = kspButtons.find_button_by_style(elements, kspButtons.PRESSED_STYLE, groups={'numbers'})
        if selected_number is not None:
            if pressed_button.in_groups({'backspace'}):
                just_selected = False
                selected_number.value = selected_number.value[:-1]
                if selected_number.value == '':
                    selected_number.value = '0'
            elif just_selected or selected_number.value == '0':
                just_selected = False
                selected_number.value = pressed_button.value
            else:
                selected_number.value += pressed_button.value
                if int(selected_number.value) > 255:
                    selected_number.value = '255'
    elif pressed_button is not None and pressed_button.in_groups({'numbers'}):
        kspButtons.reset_all_buttons(elements, groups={'numbers'})
        pressed_button.set_style(kspButtons.PRESSED_STYLE)
        just_selected = True


def refresh(memory):
    pass


def destroy_module(memory):
    elements.clear()
