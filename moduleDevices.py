import kspButtons
import kspConnect

buttons_array = []
created = False

list_size = 8
INACTIVE_STYLE = "inactive"  # for all when no connection
LIST_EXP_STYLE = "listExp"  # for expand button
HIDDEN_STYLE = "hidden"  # for anything to not show
LIST_ITEM_STYLE = "listItem"  # for list item name
LIST_ITEM_TOUCHED_STYLE = "listItemTouch"
nav_width = 70
scroll_width = 20
jump_amount = 6
scroll_y_margin = 10
expand_button_width = 50
filter_height = 50
filter_buttons = 8


def init_module(memory):
    global created
    buttons_array.clear()
    memory['moduleDevices'] = {
        'row_offset': 0,
        'view': [],
        'state': 'fetch',
        'data': None,
        'scroll_top': memory["topRowY"] + 5,
        "scroll_height": memory["screenY"] - 2 * memory["topRowY"] - 10,
        'selectedFilter': None,
        'filters': None,
        'filters_page': 0,
        'filters_pages': 0,
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
            "text_color": kspButtons.GREEN,  # r g b
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
        },
        LIST_ITEM_TOUCHED_STYLE: {
            "button_color": kspButtons.GREEN,  # r b g
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
                            w=nav_width, h=memory["screenY"] - 2 * memory["topRowY"] - 10 - filter_height,
                            clickable=True, style=INACTIVE_STYLE, styles=device_styles, groups={'nav', 'reset'}
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
                            w=expand_button_width, h=memory["screenY"] - 2 * memory["topRowY"] - 10 - filter_height,
                            clickable=False, style=INACTIVE_STYLE, styles=device_styles, groups={'exp', 'reset'}
                            )
    x_start = x_exp_start + 2 + expand_button_width
    kspButtons.make_buttons(buttons_array,
                            list_view, button_specials=list_specials,
                            x=x_start, y=memory["topRowY"] + 5,
                            w=memory['screenX'] - x_start, h=memory["screenY"] - 2 * memory["topRowY"] - 10 - filter_height,
                            clickable=False, style=INACTIVE_STYLE, styles=device_styles, groups={'part', 'reset'}
                            )

    # filters
    filters = [[]]
    for i in range(filter_buttons):
        filters[0].append("-")
    kspButtons.make_buttons(buttons_array, filters, x=0, y=memory["screenY"] - memory["topRowY"] - filter_height,
                            w=memory['screenX'], h=filter_height,
                            clickable=False, style=INACTIVE_STYLE, styles=device_styles, groups={'filter'}
                            )
    buttons_array[-1].groups = {'filter', 'page'}
    created = True


def draw(memory, screen):
    kspButtons.draw(screen, buttons_array)
    # draw scroll
    kspButtons.draw_box(screen,
                        2 + nav_width,  # x
                        memory["topRowY"] + 5,  # y
                        5,  # width
                        memory["screenY"] - 2 * memory["topRowY"] - 10 - filter_height,  # height
                        kspButtons.WHITE
                        )
    kspButtons.draw_box(screen,
                        2 + nav_width + 5,  # x
                        memory['moduleDevices']['scroll_top'],  # y
                        scroll_width - 5,  # width
                        memory['moduleDevices']['scroll_height'] - filter_height,  # height
                        kspButtons.GREY
                        )
    kspButtons.reset_all_buttons(buttons_array, groups={'reset'})


def process_click(memory, x, y):
    if not memory["popup_active"] and memory["moduleDevices"]['data'] is not None:
        pressed_button = kspButtons.find_button_by_point(buttons_array, x, y)
        if pressed_button is not None:
            if pressed_button.in_groups({'part'}):
                pressed_button.set_style(LIST_ITEM_TOUCHED_STYLE)
            elif pressed_button.in_groups({'nav'}):
                pressed_button.set_style(kspButtons.PRESSED_STYLE)
                if pressed_button.special == 'jumpUp':
                    memory['moduleDevices']['row_offset'] = max(0, memory['moduleDevices']['row_offset'] - jump_amount)
                if pressed_button.special == 'jumpDown':
                    memory['moduleDevices']['row_offset'] = min(len(memory["moduleDevices"]['view']) - list_size, memory['moduleDevices']['row_offset'] + jump_amount)
                if pressed_button.special == 'up':
                    memory['moduleDevices']['row_offset'] = max(0, memory['moduleDevices']['row_offset'] - 1)
                if pressed_button.special == 'down':
                    memory['moduleDevices']['row_offset'] = min(len(memory["moduleDevices"]['view']) - list_size, memory['moduleDevices']['row_offset'] + 1)
                memory["moduleDevices"]['state'] = 'scroll'
            elif pressed_button.in_groups({'exp'}):
                memory["moduleDevices"]['state'] = 'recompute'
                row = int(pressed_button.special.replace('expand', ''))
                true_device_row = memory["moduleDevices"]['row_offset'] + row
                path = memory["moduleDevices"]['view'][true_device_row]['path']
                raw_data = get_dict_element_by_path(memory["moduleDevices"]['data'], path)
                raw_data['expanded'] = not raw_data['expanded']
            elif pressed_button.in_groups({'filter'}):
                pressed_button.set_style(kspButtons.PRESSED_STYLE)
                if pressed_button.special is not None and pressed_button.special == 'page':
                    memory['moduleDevices']['filters_page'] = (memory['moduleDevices']['filters_page']+1) % memory['moduleDevices']['filters_pages']
                    update_filter_buttons(memory)
                elif pressed_button.special != memory['moduleDevices']['selectedFilter']:
                    memory['moduleDevices']['selectedFilter'] = pressed_button.special
                    memory['moduleDevices']['state'] = 'fetch'
                    update_filter_buttons(memory)
                elif memory['moduleDevices']['selectedFilter'] is not None:
                    memory['moduleDevices']['selectedFilter'] = None
                    memory['moduleDevices']['state'] = 'fetch'
                    update_filter_buttons(memory)
            return True
    return False


def refresh(memory):
    if memory["moduleDevices"]['state'] == 'fetch':
        memory["moduleDevices"]['data'], memory['log_message'] = get_krpc_data(memory)
        if memory["moduleDevices"]['data'] is not None:
            memory["moduleDevices"]['state'] = 'recompute'
            update_filters_values(memory)
        else:
            memory["moduleDevices"]['state'] = 'idle'
    elif memory["moduleDevices"]['state'] == 'recompute':
        # convert data to view
        update_list(memory)
        memory["moduleDevices"]['state'] = 'scroll'
    elif memory["moduleDevices"]['state'] == 'scroll':
        # get data for screen
        all_parts_count = len(memory["moduleDevices"]['view'])
        for row in range(list_size):
            ui_row = kspButtons.find_button_by_special(buttons_array, "list{}".format(row))
            ui_expand = kspButtons.find_button_by_special(buttons_array, "expand{}".format(row))
            true_device_row = memory["moduleDevices"]['row_offset'] + row
            if true_device_row >= all_parts_count:
                ui_row.idle_style_id = HIDDEN_STYLE
                ui_row.set_style(HIDDEN_STYLE)
                ui_row.clickable = False
                ui_expand.idle_style_id = HIDDEN_STYLE
                ui_expand.set_style(HIDDEN_STYLE)
                ui_expand.clickable = False
            else:
                ui_row.value = memory["moduleDevices"]['view'][true_device_row]['show']
                ui_row.idle_style_id = LIST_ITEM_STYLE
                ui_row.set_style(LIST_ITEM_STYLE)
                ui_row.clickable = True
                if memory["moduleDevices"]['view'][true_device_row]['expandable']:
                    if memory["moduleDevices"]['view'][true_device_row]['expanded']:
                        ui_expand.value = 'V'
                        ui_expand.idle_style_id = LIST_EXP_STYLE
                        ui_expand.set_style(LIST_EXP_STYLE)
                    else:
                        ui_expand.value = '>'
                        ui_expand.idle_style_id = kspButtons.IDLE_STYLE
                        ui_expand.set_style(kspButtons.IDLE_STYLE)
                    ui_expand.clickable = True
                else:
                    ui_expand.idle_style_id = HIDDEN_STYLE
                    ui_expand.set_style(HIDDEN_STYLE)
                    ui_expand.clickable = False
        scroll_full_height = memory["screenY"] - 2 * memory["topRowY"] - 10 - filter_height
        if all_parts_count != 0:
            top_idx = memory["moduleDevices"]['row_offset']
            memory["moduleDevices"]['scroll_top'] = memory["topRowY"] + 5 + int(top_idx * scroll_full_height * 1.0 / all_parts_count)
            top_idx = min(all_parts_count, list_size + top_idx)
            memory["moduleDevices"]['scroll_height'] = int(top_idx * scroll_full_height * 1.0 / all_parts_count) - memory["moduleDevices"]['scroll_top'] + memory["topRowY"] + 5 + filter_height
        else:
            memory["moduleDevices"]['scroll_top'] = memory["topRowY"] + 5
            memory["moduleDevices"]['scroll_height'] = scroll_full_height + filter_height
        memory["moduleDevices"]['state'] = 'idle'


def destroy_module(memory):
    global created
    created = False
    buttons_array.clear()
    if 'moduleDevices' in memory:
        del memory['moduleDevices']


def get_dict_element_by_path(data, path):
    if len(path) == 0 or path == '/':
        return data
    fields = path.split('/')
    if isinstance(data, list):
        f = int(fields[0])
        return get_dict_element_by_path(data[f], '/'.join(fields[1:]))
    else:
        return get_dict_element_by_path(data[fields[0]], '/'.join(fields[1:]))


def update_filters_values(memory):
    if 'filters' in memory["moduleDevices"] and memory["moduleDevices"]['filters'] is not None:
        if memory['moduleDevices']['updateFilters'] is True:
            memory['moduleDevices']['updateFilters'] = False
            if len(memory["moduleDevices"]['filters']) > filter_buttons:
                page_index = filter_buttons-1 # idx of the most right button
                pages = 1
                while page_index < len(memory["moduleDevices"]['filters']):
                    memory["moduleDevices"]['filters'].insert(page_index, pages)  # will search for -1 and replace by idx
                    pages += 1
                    page_index += filter_buttons
                # page_index is now outside the filters, complete the row now
                if len(memory["moduleDevices"]['filters']) % filter_buttons != 0:
                    # row is already complete if the above is == 0
                    while len(memory["moduleDevices"]['filters']) <= page_index:
                        memory["moduleDevices"]['filters'].append('-')
                    memory["moduleDevices"]['filters'][-1] = pages
                # populate page buttons
                page_index = filter_buttons - 1
                memory['moduleDevices']['filters_pages'] = pages
                if memory['moduleDevices']['filters_page'] >= pages:
                    memory['moduleDevices']['filters_page'] = 0
                for i in range(pages):
                    current = memory["moduleDevices"]['filters'][page_index+filter_buttons*i]
                    memory["moduleDevices"]['filters'][page_index+filter_buttons*i] = "{}/{}".format(current, pages)
                # set right button to have page function
                # page_button = kspButtons.find_all_by_groups(buttons_array, groups={'page'})[0]
                # page_button.special = 'page'
            else:
                # append empty values until row is complete
                while len(memory["moduleDevices"]['filters']) < list_size:
                    memory["moduleDevices"]['filters'].append('-')

    # else:
    #     # set right button to have filter function
    #     page_button = kspButtons.find_all_by_groups(buttons_array, groups={'page'})[0]
    #     page_button.special = None
    update_filter_buttons(memory)


def update_filter_buttons(memory):
    counter = 0
    for button in kspButtons.find_all_by_groups(buttons_array, groups={'filter'}):
        actual_idx = counter + memory["moduleDevices"]['filters_page'] * filter_buttons
        button.special = memory["moduleDevices"]['filters'][actual_idx]
        button.value = memory["moduleDevices"]['filters'][actual_idx][:6]
        counter += 1
        if button.value == '-':
            button.set_style(INACTIVE_STYLE)
            button.clickable = False
            button.special = None
        elif button.special == memory['moduleDevices']['selectedFilter']:
            button.set_style(kspButtons.PRESSED_STYLE)
            button.clickable = True
        else:
            button.set_style(kspButtons.IDLE_STYLE)
            button.clickable = True
            if '/' in button.value:
                button.special = 'page'


def update_list(memory):
    memory["moduleDevices"]['view'] = []
    for idx in range(len(memory["moduleDevices"]['data'])):
        update_viewable_part(memory, path="{}/".format(idx))
    new_style = INACTIVE_STYLE
    if len(memory["moduleDevices"]['view']) > list_size:
        new_style = kspButtons.IDLE_STYLE
        if memory['moduleDevices']['row_offset'] + list_size > len(memory["moduleDevices"]['view']):
            memory['moduleDevices']['row_offset'] = len(memory["moduleDevices"]['view']) - list_size
    else:
        memory['moduleDevices']['row_offset'] = 0
    for button in buttons_array:
        if button.in_groups({'nav'}):
            button.idle_style_id = new_style
            button.set_style(new_style)
            button.clickable = new_style == kspButtons.IDLE_STYLE


def update_viewable_part(memory, path='', use_char=''):
    try:
        part = get_dict_element_by_path(memory["moduleDevices"]['data'], path)
        expandable = 'nodes' in part and part['nodes'] is not None and len(part['nodes']) > 0
        tabulation = ''
        if len(path) > 0 and not expandable:
            tabulation = max(0, path.count('nodes')) * '  ' + hex(max(0, path.count('nodes')))[2:]
        if len(path) > 0 and expandable:
            tabulation = max(0, path.count('nodes')) * '--' + hex(max(0, path.count('nodes')))[2:]
        view_name = "{}{}{} - {}".format(tabulation, use_char, part['name'], part['type'])
        memory["moduleDevices"]['view'].append({
            'show': view_name,
            'path': path,
            'expandable': expandable,
            'expanded': part['expanded']
        })
        if part['expanded']:
            for p in range(len(part['nodes'])):
                update_viewable_part(memory, path='{}nodes/{}/'.format(path, p), use_char='\\')
            # update_viewable_part(memory, path='{}nodes/{}/'.format(path, len(part['nodes']) - 1), use_char='└')
    except TypeError or KeyError as e:
        print("Error: path={}".format(path))
        raise e


# local MOCK {'name': 'root', 'type': 'pod', 'expanded': False, 'nodes': []}
def get_krpc_data(memory):
    if memory['kspConnected'] is True:
        memory['moduleDevices']['filters'] = kspConnect.get_part_filters()
        memory['moduleDevices']['updateFilters'] = True
        return kspConnect.get_part_list(memory['moduleDevices']['selectedFilter'])
    else:
        return None, "KRPC is not connected"