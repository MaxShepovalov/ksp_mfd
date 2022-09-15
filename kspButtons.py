# button helper
import pygame

DEFAULT_FONT = 'unispace bd.ttf'
IDLE_STYLE = "idle"
PRESSED_STYLE = "pressed"

BLACK = (0, 0, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (15, 200, 15)

default_styles = {
    IDLE_STYLE: {
        "button_color": GREY,
        "text_color": WHITE,
        "font": DEFAULT_FONT,
        "align": "center",
        "alightV": "center",
        'fixedWidth': False,
        "size": 60
    },
    PRESSED_STYLE: {
        "button_color": GREY,  # r b g
        "text_color": GREEN,  # r g b
        "font": DEFAULT_FONT,  # filename
        "align": "center",  # center, left, or right
        "alignV": "center",  # center, top, or bottom
        'fixedWidth': False,  # False, None, or int (pixel)
        "size": 60  # int
    }
}


class KSPButton:
    def __init__(self, x, y, w, h, value, special=None, clickable=True, style=IDLE_STYLE, groups=None, styles=None):
        if groups is None:
            groups = set()
        if styles is None:
            styles = default_styles
        self.rect = (x, y, w, h)
        self.value = str(value)
        self.special = special
        self.style_id = str(style)
        self.idle_style_id = str(style)
        self.styles = {**styles}
        self.groups = groups
        self.clickable = clickable
        for style_id in self.styles:
            style_obj = self.styles[style_id]
            if 'button_color' not in style_obj:
                raise (KeyError("button \"{}\" style_id \"{}\" button_color is null".format(value, style_id)))
            if 'text_color' not in style_obj:
                raise (KeyError("button \"{}\" style_id \"{}\" text_color is null".format(value, style_id)))
            if 'font' not in style_obj:
                raise (KeyError("button \"{}\" style_id \"{}\" font is null".format(value, style_id)))
            if 'size' not in style_obj:
                raise (KeyError("button \"{}\" style_id \"{}\" size is null".format(value, style_id)))
        if self.style_id not in self.styles:
            raise (ValueError("button \"{}\" default style_id {} is not set".format(value, self.style_id)))

    def set_style(self, style_id):
        if style_id not in self.styles:
            raise (ValueError('button "{}" has no style "{}"'.format(self.value, style_id)))
        self.style_id = style_id

    def is_pressed(self, x_touch, y_touch):
        x, y, w, h = self.rect
        return self.clickable is True and x <= x_touch < (x + w) and y <= y_touch < (y + h)

    def in_groups(self, groups=None):
        if groups is None:
            groups = set()
        if not isinstance(groups, set):
            raise (TypeError('"groups" should be a set'))
        return len(groups.difference(self.groups)) == 0


# find button in list by touch XY
def find_button_by_point(buttons, x, y, groups=None):
    for button in buttons:
        if button.is_pressed(x, y) and button.in_groups(groups):
            return button


def find_button_by_style(buttons, style, groups=None):
    for button in buttons:
        if button.style_id == style and button.in_groups(groups):
            return button


def find_button_by_special(buttons, special, groups=None):
    for button in buttons:
        if button.special == special and button.in_groups(groups):
            return button


def find_button_by_value(buttons, value, groups=None):
    for button in buttons:
        if button.value == value and button.in_groups(groups):
            return button


def reset_all_buttons(buttons, groups=None):
    for button in buttons:
        if button.in_groups(groups):
            button.style_id = str(button.idle_style_id)


# create many buttons in bulk
def make_buttons(btn_array, button_values, x, y, w, h, button_specials=None, border=1, clickable=True, style=IDLE_STYLE,
                 groups=None, styles=None):
    number_rows = len(button_values)
    button_size_y = float(h-border) / number_rows
    for r in range(number_rows):
        number_columns = len(button_values[r])
        button_size_x = float(w-border) / number_columns
        for c in range(number_columns):
            x_btn = x + c * button_size_x
            y_btn = y + r * button_size_y
            special = None
            if button_specials is not None and \
                    len(button_values) == len(button_specials) and \
                    len(button_values[r]) == len(button_specials[r]):
                special = button_specials[r][c]
            btn_array.append(KSPButton(
                x=x_btn + border,
                y=y_btn + border,
                w=button_size_x - border,
                h=button_size_y - border,
                value=button_values[r][c],
                special=special,
                clickable=clickable,
                style=style,
                groups=groups,
                styles=styles)
            )


def render_text(screen, text, rect, style):
    text_lines = []
    total_height = 0
    bx, by, bw, bh = rect
    cx = bx + .5 * bw
    cy = by + .5 * bh
    font = pygame.font.Font(style['font'], style['size'])
    for subtext in text.split("\n"):
        text_lines.append(font.render(subtext, False, style['text_color']))
        _, _, tw, th = text_lines[-1].get_rect()
        total_height += th
    # sx, sy = pygame.display.get_window_size()
    for i in range(len(text_lines)):
        _, _, tw, th = text_lines[i].get_rect()
        tx = cx - 0.5 * tw  # center is default
        ty = int(cy - 0.5 * total_height + i * 1.05 * th)  # center is default
        # vertical
        if 'alignV' in style and style['alignV'] == "top":
            ty = by + i * 1.05 * th
        if 'alignV' in style and style['alignV'] == "bottom":
            ty = by + bh - (len(text_lines) - i) * 1.05 * th
        # horizontal
        if 'align' in style and style['align'] == "left":
            if 'fixedWidth' in style and style['fixedWidth']:
                tw = style['fixedWidth']
            tx = bx
        elif 'align' in style and style['align'] == "right":
            tx = max(bx, bx + bw - tw)
        # ignore out of button
        if ty < by or ty > by + bh or tx > bx + bw:
            continue
        screen.blit(text_lines[i], (tx, ty))


def draw(screen, buttons):
    for button in buttons:
        style = button.styles[button.style_id]
        pygame.draw.rect(surface=screen, color=style['button_color'], rect=button.rect)
        render_text(screen, rect=button.rect, text=button.value, style=style)


def draw_box(screen, x, y, w, h, color):
    pygame.draw.rect(surface=screen, color=color, rect=(x, y, w, h))
