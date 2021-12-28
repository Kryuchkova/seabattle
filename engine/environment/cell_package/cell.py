from engine.environment.color_package.color import Color


def set_color(text, color):
    return color + text + Color.reset


class Cell(object):
    empty_cell = set_color('▢', Color.yellow2)
    ship_cell = set_color('▧', Color.blue)
    destroyed_ship = set_color('☠', Color.yellow)
    damaged_ship = set_color('🔥', Color.red)
    miss_cell = set_color('💥', Color.miss)