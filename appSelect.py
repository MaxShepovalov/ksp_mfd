import kspButtons

buttons_array = []
created = False
app_select_message = "Select screen on top"


def init_module(memory):
    global created
    buttons_array.clear()
    button_styles = {
        kspButtons.IDLE_STYLE: {
            "button_color": kspButtons.GREY,
            "text_color": kspButtons.WHITE,
            "font": kspButtons.DEFAULT_FONT,
            "size": 20
        },
        kspButtons.PRESSED_STYLE: {
            "button_color": kspButtons.GREEN,
            "text_color": kspButtons.BLACK,
            "font": kspButtons.DEFAULT_FONT,
            "size": 20
        }
    }
    kspButtons.make_buttons(buttons_array,
                            [["SYS", "DEV", "-", "-", "-", "-"]],
                            0, 0, memory["screenX"], memory["topRowY"], border=5, styles=button_styles,
                            button_specials=[["moduleSettings", "moduleDevices", None, None, None, None]]
    )
    created = True


def draw(memory, screen):
    kspButtons.draw(screen, buttons_array)
    if memory['activeModule'] is None:
        kspButtons.draw(screen, [
            kspButtons.KSPButton(
                x=0,
                y=memory['screenY'] / 2,
                w=memory['screenX'],
                h=50,
                value="KSP MFD V{}\n{}".format(memory['version'], app_select_message),
                clickable=False,
                styles={
                    kspButtons.IDLE_STYLE: {
                        "button_color": kspButtons.BLACK,
                        "text_color": kspButtons.WHITE,
                        "font": kspButtons.DEFAULT_FONT,
                        "size": 20
                    }
                }
            )
        ])


def process_click(memory, x, y):
    if not memory["popup_active"]:
        pressed_button = kspButtons.find_button_by_point(buttons_array, x, y)
        if pressed_button is not None:
            memory['destroyModule'] = memory['activeModule']
            if pressed_button.style_id == kspButtons.PRESSED_STYLE:
                pressed_button.set_style(kspButtons.IDLE_STYLE)
                memory['activeModule'] = None
                memory['initModule'] = None
            else:
                kspButtons.reset_all_buttons(buttons_array)
                pressed_button.set_style(kspButtons.PRESSED_STYLE)
                memory['activeModule'] = pressed_button.special
                memory['initModule'] = pressed_button.special
            return True
    return False


def refresh(memory):
    pass


def destroy_module(memory):
    global created
    created = False
    buttons_array.clear()
