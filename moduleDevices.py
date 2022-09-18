import kspButtons
import kspConnect

buttons_array = []
created = False

LIST_SIZE = 8
INACTIVE_STYLE = "inactive"  # for all when no connection
LIST_EXP_STYLE = "listExp"  # for expand button
HIDDEN_STYLE = "hidden"  # for anything to not show
LIST_ITEM_STYLE = "listItem"  # for list item name
LIST_ITEM_TOUCHED_STYLE = "listItemTouch"
NAV_WIDTH = 70
SCROLL_WIDTH = 20
JUMP_AMOUNT = 6
SCROLL_Y_MARGIN = 10
EXPAND_BUTTON_WIDTH = 50
FILTER_HEIGHT = 50
FILTER_BUTTONS = 8

THIS_MODULE = 'moduleDevices'
STATE_FETCH = 'fetch'
STATE_IDLE = 'idle'
STATE_RECOMPUTE = 'recompute'
STATE_SCROLL = 'scroll'
MODE_TREE = 'tree'
MODE_PART = 'part'
MODE_MODULE = 'module'


def init_module(memory):
    global created
    buttons_array.clear()
    memory[THIS_MODULE] = {
        'row_offset': {
            MODE_TREE: 0,
            MODE_PART: 0,
            MODE_MODULE: 0
        },
        'view': [],
        'state': STATE_FETCH,
        'tree_data': None,
        'part_data': None,
        'module_data': None,
        'scroll_top': memory["topRowY"] + 5,
        "scroll_height": memory["screenY"] - 2 * memory["topRowY"] - 10,
        'selectedFilter': None,
        'filters': None,
        'filters_page': 0,
        'filters_pages': 0,
        'mode': MODE_TREE
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
                            w=NAV_WIDTH, h=memory["screenY"] - 2 * memory["topRowY"] - 10 - FILTER_HEIGHT,
                            clickable=True, style=INACTIVE_STYLE, styles=device_styles, groups={'nav', 'reset'}
                            )

    # list
    list_expand = LIST_SIZE * [[">"]]
    list_exp_specials = []
    list_view = []
    list_specials = []
    for i in range(LIST_SIZE):
        list_view.append(["- part {} name - part type -".format(i)])
        list_specials.append(["list{}".format(i)])
        list_exp_specials.append(["expand{}".format(i)])
    x_exp_start = NAV_WIDTH + 2 + SCROLL_WIDTH + 5
    kspButtons.make_buttons(buttons_array,
                            list_expand, button_specials=list_exp_specials,
                            x=x_exp_start, y=memory["topRowY"] + 5, border=5,
                            w=EXPAND_BUTTON_WIDTH, h=memory["screenY"] - 2 * memory["topRowY"] - 10 - FILTER_HEIGHT,
                            clickable=False, style=INACTIVE_STYLE, styles=device_styles, groups={'exp', 'reset'}
                            )
    x_start = x_exp_start + 2 + EXPAND_BUTTON_WIDTH
    kspButtons.make_buttons(buttons_array,
                            list_view, button_specials=list_specials,
                            x=x_start, y=memory["topRowY"] + 5,
                            w=memory['screenX'] - x_start, h=memory["screenY"] - 2 * memory["topRowY"] - 10 - FILTER_HEIGHT,
                            clickable=False, style=INACTIVE_STYLE, styles=device_styles, groups={'part', 'reset'}
                            )

    # filters
    filters = [[]]
    for i in range(FILTER_BUTTONS):
        filters[0].append("-")
    kspButtons.make_buttons(buttons_array, filters, x=0, y=memory["screenY"] - memory["topRowY"] - FILTER_HEIGHT,
                            w=memory['screenX'], h=FILTER_HEIGHT,
                            clickable=False, style=INACTIVE_STYLE, styles=device_styles, groups={'filter'}
                            )
    buttons_array[-1].groups = {'filter', 'page'}
    created = True


def draw(memory, screen):
    kspButtons.draw(screen, buttons_array)
    # draw scroll
    scroll_style = buttons_array[0].styles[buttons_array[0].style_id]
    kspButtons.draw_box(screen,
                        2 + NAV_WIDTH,  # x
                        memory["topRowY"] + 5,  # y
                        5,  # width
                        memory["screenY"] - 2 * memory["topRowY"] - 10 - FILTER_HEIGHT,  # height
                        scroll_style['text_color']
                        )
    kspButtons.draw_box(screen,
                        2 + NAV_WIDTH + 5,  # x
                        memory[THIS_MODULE]['scroll_top'],  # y
                        SCROLL_WIDTH - 5,  # width
                        memory[THIS_MODULE]['scroll_height'] - FILTER_HEIGHT,  # height
                        scroll_style['button_color']
                        )
    kspButtons.reset_all_buttons(buttons_array, groups={'reset'})


def process_click(memory, x, y):
    if not memory["popup_active"] and memory[THIS_MODULE]['tree_data'] is not None:
        pressed_button = kspButtons.find_button_by_point(buttons_array, x, y)
        if pressed_button is not None:
            if pressed_button.in_groups({'part'}):
                pressed_button.set_style(LIST_ITEM_TOUCHED_STYLE)
                view_idx = int(pressed_button.special.replace('list', ''))
                data_object_path = memory[THIS_MODULE]['view'][view_idx]['path']
                if memory[THIS_MODULE]['mode'] == MODE_TREE:
                    ksp_object = get_dict_element_by_path(memory[THIS_MODULE]['tree_data'], data_object_path)
                    if ksp_object['part'] is not None and isinstance(ksp_object['part'], kspConnect.krpcConnection.space_center.Part):
                        change_mode(memory, MODE_PART)
                        kspConnect.queue_agent_add_action(
                            THIS_MODULE,
                            kspConnect.queue_add_request(kspConnect.web_get_part_modules, {'part': ksp_object['part']}),
                            handler_get_modules_for_part
                        )
                        memory['log_message'] = "Waiting for modules of part {}".format(ksp_object['part'])
                    elif ksp_object['part'] is not None:
                        change_mode(memory, MODE_PART)
                        kspConnect.queue_agent_add_action(
                            THIS_MODULE,
                            kspConnect.queue_add_request(kspConnect.web_get_part_modules, {'part': ksp_object['part'].part}),
                            handler_get_modules_for_part
                        )
                        memory['log_message'] = "Waiting for actions of part {}".format(ksp_object['part'].part)
                    else:
                        memory['log_message'] = "Selected line is not a Part or Module"
                elif memory[THIS_MODULE]['mode'] == MODE_PART:
                    ksp_object = get_dict_element_by_path(memory[THIS_MODULE]['part_data'], data_object_path)
                    if ksp_object['part'] is not None and isinstance(ksp_object['part'], kspConnect.krpcConnection.space_center.Module):
                        change_mode(memory, MODE_MODULE)
                        kspConnect.queue_agent_add_action(
                            THIS_MODULE,
                            kspConnect.queue_add_request(kspConnect.web_get_module_actions, {'module': ksp_object['part']}),
                            handler_get_modules_actions
                        )
                        memory['log_message'] = "Waiting for actions of module {}".format(ksp_object['part'])
                    else:
                        memory['log_message'] = "Selected line is not a Module"
                elif memory[THIS_MODULE]['mode'] == MODE_MODULE:
                    memory['log_message'] = "Module actions are WIP"
            elif pressed_button.in_groups({'nav'}):
                pressed_button.set_style(kspButtons.PRESSED_STYLE)
                if pressed_button.special == 'jumpUp':
                    set_row_offset(memory, max(0, get_row_offset(memory) - JUMP_AMOUNT))
                if pressed_button.special == 'jumpDown':
                    set_row_offset(memory, min(len(memory[THIS_MODULE]['view']) - LIST_SIZE, get_row_offset(memory) + JUMP_AMOUNT))
                if pressed_button.special == 'up':
                    set_row_offset(memory, max(0, get_row_offset(memory) - 1))
                if pressed_button.special == 'down':
                    set_row_offset(memory, min(len(memory[THIS_MODULE]['view']) - LIST_SIZE, get_row_offset(memory) + 1))
                memory[THIS_MODULE]['state'] = STATE_SCROLL
            elif pressed_button.in_groups({'exp'}):
                memory[THIS_MODULE]['state'] = STATE_RECOMPUTE
                row = int(pressed_button.special.replace('expand', ''))
                true_device_row = get_row_offset(memory) + row
                path = memory[THIS_MODULE]['view'][true_device_row]['path']
                source = get_mode_data_source(memory)
                raw_data = get_dict_element_by_path(memory[THIS_MODULE][source], path)
                raw_data['expanded'] = not raw_data['expanded']
            elif pressed_button.in_groups({'filter'}):
                pressed_button.set_style(kspButtons.PRESSED_STYLE)
                if memory[THIS_MODULE]['mode'] == MODE_TREE:
                    if pressed_button.special is not None and pressed_button.special == 'page':
                        memory[THIS_MODULE]['filters_page'] = (memory[THIS_MODULE]['filters_page']+1) % memory[THIS_MODULE]['filters_pages']
                        update_filter_buttons(memory)
                    elif pressed_button.special != memory[THIS_MODULE]['selectedFilter']:
                        memory[THIS_MODULE]['selectedFilter'] = pressed_button.special
                        memory[THIS_MODULE]['state'] = STATE_FETCH
                        update_filter_buttons(memory)
                    elif memory[THIS_MODULE]['selectedFilter'] is not None:
                        memory[THIS_MODULE]['selectedFilter'] = None
                        memory[THIS_MODULE]['state'] = STATE_FETCH
                        update_filter_buttons(memory)
                elif memory[THIS_MODULE]['mode'] in [MODE_PART, MODE_MODULE]:
                    if pressed_button.special is not None:
                        change_mode(memory, pressed_button.special)
            return True
    return False


def refresh(memory):
    # check for queries
    kspConnect.queue_agent_scan_requests(memory, THIS_MODULE)
    # update ui
    if memory[THIS_MODULE]['state'] == STATE_FETCH:
        get_krpc_data(memory)
        memory[THIS_MODULE]['state'] = STATE_IDLE
    if memory[THIS_MODULE]['state'] == STATE_RECOMPUTE:
        # convert data to view
        update_data_for_list(memory)
        memory[THIS_MODULE]['state'] = STATE_SCROLL
    if memory[THIS_MODULE]['state'] == STATE_SCROLL:
        # get data for screen
        update_view_list(memory)
        memory[THIS_MODULE]['state'] = STATE_IDLE


def destroy_module(memory):
    global created
    created = False
    buttons_array.clear()
    if THIS_MODULE in memory:
        del memory[THIS_MODULE]


def get_dict_element_by_path(data, path):
    if len(path) == 0 or path == '/':
        return data
    fields = path.split('/')
    if isinstance(data, list):
        f = int(fields[0])
        return get_dict_element_by_path(data[f], '/'.join(fields[1:]))
    else:
        return get_dict_element_by_path(data[fields[0]], '/'.join(fields[1:]))


def update_filter_buttons(memory):
    counter = 0
    for button in kspButtons.find_all_by_groups(buttons_array, groups={'filter'}):
        if memory[THIS_MODULE]['mode'] == MODE_TREE:
            actual_idx = counter + memory[THIS_MODULE]['filters_page'] * FILTER_BUTTONS
            button.special = memory[THIS_MODULE]['filters'][actual_idx]
            button.value = memory[THIS_MODULE]['filters'][actual_idx][:6]
        elif memory[THIS_MODULE]['mode'] == MODE_PART:
            if counter == 0:
                button.value = 'tree'
                button.special = MODE_TREE
            else:
                button.value = '-'
        elif memory[THIS_MODULE]['mode'] == MODE_MODULE:
            if counter == 0:
                button.value = 'tree'
                button.special = MODE_TREE
            elif counter == 1: # and memory[THIS_MODULE]['selectedFilter'] is None:
                button.value = 'part'
                button.special = MODE_PART
            else:
                button.value = '-'
        counter += 1
        if button.value == '-':
            button.set_style(INACTIVE_STYLE)
            button.clickable = False
            button.special = None
        elif button.special == memory[THIS_MODULE]['selectedFilter']:
            button.set_style(kspButtons.PRESSED_STYLE)
            button.clickable = True
        else:
            button.set_style(kspButtons.IDLE_STYLE)
            button.clickable = True
            if '/' in button.value:
                button.special = 'page'

def update_view_list(memory):
    all_parts_count = len(memory[THIS_MODULE]['view'])
    for row in range(LIST_SIZE):
        ui_row = kspButtons.find_button_by_special(buttons_array, "list{}".format(row))
        ui_expand = kspButtons.find_button_by_special(buttons_array, "expand{}".format(row))
        true_device_row = get_row_offset(memory) + row
        if true_device_row >= all_parts_count:
            ui_row.idle_style_id = HIDDEN_STYLE
            ui_row.set_style(HIDDEN_STYLE)
            ui_row.clickable = False
            ui_expand.idle_style_id = HIDDEN_STYLE
            ui_expand.set_style(HIDDEN_STYLE)
            ui_expand.clickable = False
        else:
            ui_row.value = memory[THIS_MODULE]['view'][true_device_row]['show']
            ui_row.idle_style_id = LIST_ITEM_STYLE
            ui_row.set_style(LIST_ITEM_STYLE)
            ui_row.clickable = True
            if memory[THIS_MODULE]['view'][true_device_row]['expandable']:
                if memory[THIS_MODULE]['view'][true_device_row]['expanded']:
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
    scroll_full_height = memory["screenY"] - 2 * memory["topRowY"] - 10 - FILTER_HEIGHT
    if all_parts_count != 0:
        top_idx = get_row_offset(memory)
        memory[THIS_MODULE]['scroll_top'] = memory["topRowY"] + 5 + int(
            top_idx * scroll_full_height * 1.0 / all_parts_count)
        top_idx = min(all_parts_count, LIST_SIZE + top_idx)
        memory[THIS_MODULE]['scroll_height'] = int(top_idx * scroll_full_height * 1.0 / all_parts_count) - \
                                               memory[THIS_MODULE]['scroll_top'] + memory[
                                                       "topRowY"] + 5 + FILTER_HEIGHT
    else:
        memory[THIS_MODULE]['scroll_top'] = memory["topRowY"] + 5
        memory[THIS_MODULE]['scroll_height'] = scroll_full_height + FILTER_HEIGHT


def get_mode_data_source(memory):
    source = 'tree_data'
    if memory[THIS_MODULE]['mode'] == MODE_PART:
        source = 'part_data'
    if memory[THIS_MODULE]['mode'] == MODE_MODULE:
        source = 'module_data'
    return source


def update_data_for_list(memory):
    source = get_mode_data_source(memory)
    memory[THIS_MODULE]['view'] = []
    if memory[THIS_MODULE][source] is not None:
        for idx in range(len(memory[THIS_MODULE][source])):
            update_viewable_part(memory, source, path="{}/".format(idx))
    new_style = INACTIVE_STYLE
    if len(memory[THIS_MODULE]['view']) > LIST_SIZE:
        new_style = kspButtons.IDLE_STYLE
        if get_row_offset(memory) + LIST_SIZE > len(memory[THIS_MODULE]['view']):
            set_row_offset(memory, len(memory[THIS_MODULE]['view']) - LIST_SIZE)
    else:
        set_row_offset(memory, 0)
    for button in buttons_array:
        if button.in_groups({'nav'}):
            button.idle_style_id = new_style
            button.set_style(new_style)
            button.clickable = new_style == kspButtons.IDLE_STYLE


def update_viewable_part(memory, source, path='', use_char=''):
    try:
        part = get_dict_element_by_path(memory[THIS_MODULE][source], path)
        expandable = 'nodes' in part and part['nodes'] is not None and len(part['nodes']) > 0
        tabulation = ''
        if len(path) > 0 and not expandable:
            tabulation = max(0, path.count('nodes')) * '  ' + hex(max(0, path.count('nodes')))[2:]
        if len(path) > 0 and expandable:
            tabulation = max(0, path.count('nodes')) * '--' + hex(max(0, path.count('nodes')))[2:]
        view_name = "{}{}{} - {}".format(tabulation, use_char, part['name'], part['type'])
        memory[THIS_MODULE]['view'].append({
            'show': view_name,
            'path': path,
            'expandable': expandable,
            'expanded': part['expanded']
        })
        if part['expanded']:
            for p in range(len(part['nodes'])):
                update_viewable_part(memory, source=source, path='{}nodes/{}/'.format(path, p), use_char='\\')
    except TypeError or KeyError as e:
        print("Error: path={}".format(path))
        raise e


# local MOCK {'name': 'root', 'type': 'pod', 'expanded': False, 'nodes': []}
def get_krpc_data(memory):
    if memory['kspConnected'] is True:
        kspConnect.queue_agent_add_action(
            THIS_MODULE,
            kspConnect.queue_add_request(kspConnect.web_get_part_filters),
            handler_get_filters
        )
        kspConnect.queue_agent_add_action(
            THIS_MODULE,
            kspConnect.queue_add_request(kspConnect.web_get_part_list, {'filter': memory[THIS_MODULE]['selectedFilter']}),
            handler_get_parts
        )
        memory["log_message"] = "Waiting for part list"


def handler_get_filters(memory, data):
    memory[THIS_MODULE]['filters'] = data
    if 'filters' in memory[THIS_MODULE] and memory[THIS_MODULE]['filters'] is not None:
        if len(memory[THIS_MODULE]['filters']) > FILTER_BUTTONS:
            page_index = FILTER_BUTTONS - 1  # idx of the most right button
            pages = 1
            while page_index < len(memory[THIS_MODULE]['filters']):
                memory[THIS_MODULE]['filters'].insert(page_index, pages)  # will search for -1 and replace by idx
                pages += 1
                page_index += FILTER_BUTTONS
            # page_index is now outside the filters, complete the row now
            if len(memory[THIS_MODULE]['filters']) % FILTER_BUTTONS != 0:
                # row is already complete if the above is == 0
                while len(memory[THIS_MODULE]['filters']) <= page_index:
                    memory[THIS_MODULE]['filters'].append('-')
                memory[THIS_MODULE]['filters'][-1] = pages
            # populate page buttons
            page_index = FILTER_BUTTONS - 1
            memory[THIS_MODULE]['filters_pages'] = pages
            if memory[THIS_MODULE]['filters_page'] >= pages:
                memory[THIS_MODULE]['filters_page'] = 0
            for i in range(pages):
                current = memory[THIS_MODULE]['filters'][page_index + FILTER_BUTTONS * i]
                memory[THIS_MODULE]['filters'][page_index + FILTER_BUTTONS * i] = "{}/{}".format(current, pages)
            # set right button to have page function
            # page_button = kspButtons.find_all_by_groups(buttons_array, groups={'page'})[0]
            # page_button.special = 'page'
        else:
            # append empty values until row is complete
            while len(memory[THIS_MODULE]['filters']) < LIST_SIZE:
                memory[THIS_MODULE]['filters'].append('-')
    update_filter_buttons(memory)


def handler_get_parts(memory, data):
    memory[THIS_MODULE]['tree_data'], memory['log_message'] = data
    if memory[THIS_MODULE]['tree_data'] is not None:
        memory[THIS_MODULE]['state'] = STATE_RECOMPUTE
    else:
        memory[THIS_MODULE]['state'] = STATE_IDLE

def handler_get_modules_for_part(memory, data):
    if isinstance(data, Exception):
        memory['log_message'] = str(data)
    else:
        memory[THIS_MODULE]['part_data'] = data
        memory[THIS_MODULE]['state'] = STATE_RECOMPUTE


def handler_get_modules_actions(memory, data):
    if isinstance(data, Exception):
        memory['log_message'] = str(data)
    else:
        memory[THIS_MODULE]['module_data'] = data
        memory[THIS_MODULE]['state'] = STATE_RECOMPUTE


def change_mode(memory, new_mode):
    if new_mode in [MODE_PART, MODE_TREE]:
        memory[THIS_MODULE]['module_data'] = None
    if new_mode == MODE_TREE:
        memory[THIS_MODULE]['part_data'] = None
    memory[THIS_MODULE]['mode'] = new_mode
    memory[THIS_MODULE]['state'] = STATE_RECOMPUTE
    update_filter_buttons(memory)


def get_row_offset(memory):
    return memory[THIS_MODULE]['row_offset'][memory[THIS_MODULE]['mode']]


def set_row_offset(memory, new_value):
    memory[THIS_MODULE]['row_offset'][memory[THIS_MODULE]['mode']] = new_value
