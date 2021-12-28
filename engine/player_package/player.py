from random import randrange
from random import choice

from engine.environment.cell_package.cell import Cell
from engine.environment.part_package.part import FieldPart
from engine.game_package.game import Game
from engine.ship_package.ship import Ship


class Player(object):
    def __init__(self, name, is_ai, skill, auto_ship):
        self.name = name
        self.is_ai = is_ai
        self.auto_ship_setup = auto_ship
        self.skill = skill
        self.message = []
        self.ships = []
        self.enemy_ships = []
        self.field = None


    def get_input(self, input_type):
        if input_type == "ship_setup":
            if self.is_ai or self.auto_ship_setup:
                user_input = str(choice(Game.letters)) + str(randrange(0, self.field.size)) + choice(["Г", "В"])
            else:
                user_input = input().upper().replace(" ", "")

            if len(user_input) < 3:
                return 0, 0, 0

            x, y, r = user_input[0], user_input[1:-1], user_input[-1]

            if x not in Game.letters or not y.isdigit() or int(y) not in range(1, Game.field_size + 1) or \
                    r not in ("Г", "В"):
                self.message.append('Приказ непонятен, ошибка формата данных')
                return 0, 0, 0

            return Game.letters.index(x), int(y) - 1, 0 if r == 'Г' else 1

        if input_type == "shot":

            if self.is_ai:
                if self.skill == 1:
                    x, y = choice(self.field.get_max_weight_cells())
                if self.skill == 0:
                    x, y = randrange(0, self.field.size), randrange(0, self.field.size)
            else:
                user_input = input().upper().replace(" ", "")
                x, y = user_input[0].upper(), user_input[1:]
                if x not in Game.letters or not y.isdigit() or int(y) not in range(1, Game.field_size + 1):
                    self.message.append('Приказ непонятен, ошибка формата данных')
                    return 500, 0
                x = Game.letters.index(x)
                y = int(y) - 1
            return x, y

    def make_shot(self, target_player):
        sx, sy = self.get_input('shot')
        if sx + sy == 500 or self.field.radar[sx][sy] != Cell.empty_cell:
            return 'retry'

        shot_res = target_player.receive_shot((sx, sy))

        if shot_res == 'miss':
            self.field.radar[sx][sy] = Cell.miss_cell

        if shot_res == 'get':
            self.field.radar[sx][sy] = Cell.damaged_ship

        if type(shot_res) == Ship:
            destroyed_ship = shot_res
            self.field.mark_destroyed_ship(destroyed_ship, FieldPart.radar)
            self.enemy_ships.remove(destroyed_ship.size)
            shot_res = 'kill'

        self.field.recalculate_weight_map(self.enemy_ships)

        return shot_res

    def receive_shot(self, shot):
        sx, sy = shot

        if type(self.field.map[sx][sy]) == Ship:
            ship = self.field.map[sx][sy]
            ship.hp -= 1

            if ship.hp <= 0:
                self.field.mark_destroyed_ship(ship, FieldPart.main)
                self.ships.remove(ship)
                return ship

            self.field.map[sx][sy] = Cell.damaged_ship
            return 'get'

        else:
            self.field.map[sx][sy] = Cell.miss_cell
            return 'miss'
