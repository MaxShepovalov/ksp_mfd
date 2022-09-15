import kspButtons

buttons_array = []
created = False

list_size = 8
INACTIVE_STYLE = "inactive"  # for all when no connection
LIST_EXP_STYLE = "listExp"  # for expand button
HIDDEN_STYLE = "hidden"  # for anything to not show
LIST_ITEM_STYLE = "listItem"  # for list item name
nav_width = 70
scroll_width = 30
jump_amount = 6
scroll_y_margin = 10
expand_button_width = 30


def init_module(memory):
    global created
    buttons_array.clear()
    memory['moduleDevices'] = {
        'row_offset': 0,
        'view': [],
        'expandable': [],
        'data': None
    }

    device_styles = {
        INACTIVE_STYLE: {
            "button_color": kspButtons.BLACK,
            "text_color": kspButtons.GREY,
            "font": kspButtons.DEFAULT_FONT,
            "align": "center",
            "alightV": "center",
            'fixedWidth': False,
            "size": 20
        },
        HIDDEN_STYLE: {
            "button_color": kspButtons.BLACK,
            "text_color": kspButtons.BLACK,
            "font": kspButtons.DEFAULT_FONT,
            "align": "center",
            "alightV": "center",
            'fixedWidth': False,
            "size": 20
        },
        kspButtons.IDLE_STYLE: {
            "button_color": kspButtons.GREY,
            "text_color": kspButtons.WHITE,
            "font": kspButtons.DEFAULT_FONT,
            "align": "center",
            "alightV": "center",
            'fixedWidth': False,
            "size": 20
        },
        kspButtons.PRESSED_STYLE: {
            "button_color": kspButtons.GREEN,  # r b g
            "text_color": kspButtons.BLACK,  # r g b
            "font": kspButtons.DEFAULT_FONT,  # filename
            "align": "center",  # center, left, or right
            "alignV": "center",  # center, top, or bottom
            'fixedWidth': False,  # False, None, or int (pixel)
            "size": 20  # int
        },
        LIST_EXP_STYLE: {
            "button_color": kspButtons.GREY,  # r b g
            "text_color": kspButtons.WHITE,  # r g b
            "font": kspButtons.DEFAULT_FONT,  # filename
            "align": "center",  # center, left, or right
            "alignV": "center",  # center, top, or bottom
            'fixedWidth': False,  # False, None, or int (pixel)
            "size": 20  # int
        },
        LIST_ITEM_STYLE: {
            "button_color": kspButtons.BLACK,  # r b g
            "text_color": kspButtons.WHITE,  # r g b
            "font": kspButtons.DEFAULT_FONT,  # filename
            "align": "left",  # center, left, or right
            "alignV": "center",  # center, top, or bottom
            'fixedWidth': False,  # False, None, or int (pixel)
            "size": 20  # int
        }
    }

    # navigation
    buttons_view = [["^^"], ["^"], ["v"], ["vv"]]
    buttons_actions = [["jumpUp"], ["up"], ["down"], ["jumpDown"]]
    kspButtons.make_buttons(buttons_array,
                            buttons_view, button_specials=buttons_actions,
                            x=0, y=memory["topRowY"] + 5, border=5,
                            w=nav_width, h=memory["screenY"] - 2 * memory["topRowY"] - 10,
                            clickable=True, styles=device_styles, groups={'nav'}
                            )

    # list
    list_expand = list_size * [[">"]]
    list_exp_specials = []
    list_view = []
    list_specials = []
    for i in range(list_size):
        list_view.append(["- part {} name - part type -".format(i)])
        list_specials.append(["list{}".format(i)])
        list_exp_specials.append(["expand{}".format(i)])
    x_exp_start = nav_width + 2 + scroll_width + 5
    kspButtons.make_buttons(buttons_array,
                            list_expand, button_specials=list_exp_specials,
                            x=x_exp_start, y=memory["topRowY"] + 5, border=5,
                            w=expand_button_width, h=memory["screenY"] - 2 * memory["topRowY"] - 10,
                            clickable=True, style=LIST_EXP_STYLE, styles=device_styles, groups={'exp'}
                            )
    x_start = x_exp_start+2+expand_button_width
    kspButtons.make_buttons(buttons_array,
                            list_view, button_specials=list_specials,
                            x=x_start, y=memory["topRowY"] + 5,
                            w=memory['screenX']-x_start, h=memory["screenY"] - 2 * memory["topRowY"] - 10,
                            clickable=True, style=LIST_ITEM_STYLE, styles=device_styles, groups={'part'}
                            )

    # reset all to inactive

    created = True


def draw(memory, screen):
    kspButtons.draw(screen, buttons_array)
    # draw scroll
    # static line
    screen_pad_top = memory["topRowY"] + 5
    screen_pad_height = memory["screenY"] - 2 * memory["topRowY"] - 10
    kspButtons.draw_box(screen,
                        2 + nav_width,  # x
                        screen_pad_top,  # y
                        5,  # width
                        screen_pad_height,  # height
                        kspButtons.GREY
                        )

    kspButtons.draw_box(screen,
                        2 + nav_width + 5,  # x
                        screen_pad_top,  # y
                        scroll_width - 5,  # width
                        screen_pad_height,  # height
                        kspButtons.WHITE
                        )


def process_click(memory, x, y):
    # kspButtons.reset_all_buttons(buttons_array)
    if not memory["popup_active"]:
        pressed_button = kspButtons.find_button_by_point(buttons_array, x, y)
        if pressed_button is not None:
            pressed_button.set_style(kspButtons.PRESSED_STYLE)
            if pressed_button.special == "exit":
                memory['appState'] = "exit"
            return True
    return False


def refresh(memory):
    pass


def destroy_module(memory):
    global created
    created = False
    buttons_array.clear()
    if 'moduleDevices' in memory:
        del memory['moduleDevices']
