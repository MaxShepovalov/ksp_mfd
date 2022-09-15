import kspButtons

popup = []


def init_module(memory):
    pass


def draw(memory, screen):
    if len(popup) > 0:
        kspButtons.draw(screen, popup)


def process_click(memory, x, y):
    pass


def refresh(memory):
    popup.clear()
    if 'log_message' in memory and memory['log_message'] is not None:
        kspButtons.make_buttons(
            popup, [[str(memory['log_message'])]],
            0, memory['screenY'] - memory["topRowY"], memory['screenX'], memory['topRowY'],
            styles={
                kspButtons.IDLE_STYLE: {
                    "button_color": kspButtons.BLACK,  # r b g
                    "text_color": kspButtons.WHITE,  # r g b
                    "font": kspButtons.DEFAULT_FONT,  # filename
                    "align": "left",  # center, left, or right
                    "alignV": "center",  # center, top, or bottom
                    'fixedWidth': False,  # False, None, or int (pixel)
                    "size": 14  # int
                }
            }
        )


def destroy_module(memory):
    popup.clear()
