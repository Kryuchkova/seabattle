import os

from engine.environment.cell_package.cell import Cell
from engine.environment.field_package.field import Field
from engine.environment.part_package.part import FieldPart

from engine.ship_package.ship import Ship


class Game(object):
    letters = ("А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К")
    ships_rules = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    field_size = len(letters)

    def __init__(self):
        self.players = []
        self.current_player = None
        self.next_player = None

        self.status = 'prepare'

    def start_game(self):
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def status_check(self):
        if self.status == 'prepare' and len(self.players) >= 2:
            self.status = 'in_game'
            self.start_game()
            return True
        if self.status == 'in_game' and len(self.next_player.ships) == 0:
            self.status = 'game_over'
            return True

    def add_player(self, player):
        player.field = Field(Game.field_size)
        player.enemy_ships = list(Game.ships_rules)
        self.ships_setup(player)
        player.field.recalculate_weights(player.enemy_ships)
        self.players.append(player)

    def ships_setup(self, player):
        for ship_size in Game.ships_rules:
            retry_count = 30
            ship = Ship(ship_size, 0, 0, 0)

            while True:
                Game.clear_screen()
                if player.auto_ship_setup is not True:
                    player.field.draw_field(FieldPart.main)
                    player.message.append('Куда поставить {} корабль: '.format(ship_size))
                    for _ in player.message:
                        print(_)
                else:
                    print('{}. Расставляем корабли...'.format(player.name))

                player.message.clear()

                x, y, r = player.process('ship_setup')
                if x + y + r == 0:
                    continue

                ship.set_position(x, y, r)

                if player.field.check_ship_fits(ship, FieldPart.main):
                    player.field.add_ship_to_field(ship, FieldPart.main)
                    player.ships.append(ship)
                    break

                player.message.append('Неправильная позиция!')
                retry_count -= 1
                if retry_count < 0:
                    player.field.map = [[Cell.empty_cell for _ in range(Game.field_size)] for _ in
                                        range(Game.field_size)]
                    player.ships = []
                    self.ships_setup(player)
                    return True

    def draw(self):
        if not self.current_player.is_ai:
            print("Ваши корабли")
            self.current_player.field.draw_field(FieldPart.main)
            print("Радар")
            self.current_player.field.draw_field(FieldPart.radar)
        for line in self.current_player.message:
            print(line)

    def switch_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
