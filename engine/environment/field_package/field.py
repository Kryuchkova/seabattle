from engine.environment.cell_package.cell import Cell
from engine.environment.part_package.part import FieldPart
from engine.ship_package.ship import Ship

DELTA = 50


class Field(object):
    def __init__(self, size):
        self.size = size
        self.map = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]
        self.radar = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]
        self.weight = [[1 for _ in range(size)] for _ in range(size)]

    def get_field_part(self, element):
        if element == FieldPart.main:
            return self.map
        if element == FieldPart.radar:
            return self.radar
        if element == FieldPart.weight:
            return self.weight

    def draw_field(self, element):
        field = self.get_field_part(element)
        weights = self.get_max_weight_cells()

        if element == FieldPart.weight:
            for x in range(self.size):
                for y in range(self.size):
                    if (x, y) in weights:
                        print('\033[1;32m', end='')
                    if field[x][y] < self.size:
                        print(" ", end='')
                    if field[x][y] == 0:
                        print(str("" + ". " + ""), end='')
                    else:
                        print(str("" + str(field[x][y]) + " "), end='')
                    print('\033[0;0m', end='')
                print()

        else:
            for x in range(-1, self.size):
                for y in range(-1, self.size):
                    if x == -1 and y == -1:
                        print("  ", end="")
                        continue
                    if x == -1 and y >= 0:
                        print(y + 1, end=" ")
                        continue
                    if x >= 0 and y == -1:
                        from engine.game_package.game import Game
                        print(Game.letters[x], end='')
                        continue
                    print(" " + str(field[x][y]), end='')
                print("")
        print("")

    def check_ship_fits(self, ship, element):
        field = self.get_field_part(element)

        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or \
                ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False

        x = ship.x
        y = ship.y
        width = ship.width
        height = ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                if str(field[p_x][p_y]) == Cell.miss_cell:
                    return False

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                if str(field[p_x][p_y]) in (Cell.ship_cell, Cell.destroyed_ship):
                    return False

        return True

    def mark_destroyed_ship(self, ship, element):
        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                field[p_x][p_y] = Cell.miss_cell

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = Cell.destroyed_ship

    def add_ship_to_field(self, ship, element):
        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = ship

    def get_max_weight_cells(self):
        weights = {}
        max_weight = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.weight[x][y] > max_weight:
                    max_weight = self.weight[x][y]
                weights.setdefault(self.weight[x][y], []).append((x, y))

        return weights[max_weight]

    def recalculate_weight_map(self, available_ships):
        self.weight = [[1 for _ in range(self.size)] for _ in range(self.size)]

        for x in range(self.size):
            for y in range(self.size):
                if self.radar[x][y] == Cell.damaged_ship:
                    self.weight[x][y] = 0

                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            self.weight[x - 1][y - 1] = 0
                        self.weight[x - 1][y] *= DELTA
                        if y + 1 < self.size:
                            self.weight[x - 1][y + 1] = 0

                    if y - 1 >= 0:
                        self.weight[x][y - 1] *= DELTA
                    if y + 1 < self.size:
                        self.weight[x][y + 1] *= DELTA

                    if x + 1 < self.size:
                        if y - 1 >= 0:
                            self.weight[x + 1][y - 1] = 0
                        self.weight[x + 1][y] *= DELTA
                        if y + 1 < self.size:
                            self.weight[x + 1][y + 1] = 0

        for ship_size in available_ships:
            ship = Ship(ship_size, 1, 1, 0)
            for x in range(self.size):
                for y in range(self.size):
                    if self.radar[x][y] in (Cell.destroyed_ship, Cell.damaged_ship, Cell.miss_cell) \
                            or self.weight[x][y] == 0:
                        self.weight[x][y] = 0
                        continue
                    for rotation in range(0, 4):
                        ship.set_position(x, y, rotation)
                        if self.check_ship_fits(ship, FieldPart.radar):
                            self.weight[x][y] += 1
