from engine.environment.part_package.part import FieldPart
from engine.game_package.game import Game
from engine.player_package.player import Player

if __name__ == '__main__':
    players = [Player(name='Real Player', is_ai=False, auto_ship=True, skill=1),
               Player(name='Artificial Intelligence', is_ai=True, auto_ship=True, skill=1)]

    game = Game()

    while True:
        game.status_check()

        if game.status == 'prepare':
            game.add_player(players.pop(0))

        if game.status == 'in_game':
            Game.clear_screen()
            game.current_player.message.append("Ждём приказа, капитан {}. Выстрел по: ".format(game.current_player.name))
            game.draw()
            game.current_player.message.clear()
            shot_result = game.current_player.make_shot(game.next_player)
            if shot_result == 'miss':
                game.next_player.message.append('На этот раз {}, промахнулся! '.format(game.current_player.name))
                game.next_player.message.append('Ваш ход {}!'.format(game.next_player.name))
                game.switch_players()
                continue
            elif shot_result == 'retry':
                game.current_player.message.append('Попробуйте еще раз!')
                continue
            elif shot_result == 'get':
                game.current_player.message.append('Отличный выстрел, продолжайте, Капитан {}!'.format(game.current_player.name))
                game.next_player.message.append('Капитан {}, наш корабль попал под обстрел!'.format(game.next_player.name))
                continue
            elif shot_result == 'kill':
                game.current_player.message.append('Капитан {}, корабль противника уничтожен!'.format(game.current_player.name))
                game.next_player.message.append('Плохие новости капитан {}, наш корабль был уничтожен...'.format(game.next_player.name))
                continue

        if game.status == 'game_over':
            Game.clear_screen()
            game.next_player.field.draw_field(FieldPart.main)
            game.current_player.field.draw_field(FieldPart.main)
            print('Это был последний корабль {}'.format(game.next_player.name))
            print('{} выиграл матч! Поздравления!'.format(game.current_player.name))
            break

    print('Спасибо за игру!')
    input('')
