import random

class PlayerInterface:
    def update_position(self, new_position: int):
        pass

    def get_position(self):
        pass

    def clear(self):
        pass


class BoardInterface:
    """
    :param player:
    :param movements_quantity:
    :return: the next square where the player go
    """
    def move_player(self, player: PlayerInterface, movements_quantity: int):
         pass


class Player(PlayerInterface):

    def __init__(self, name, first_square):
        self.name = name
        self.first_square = first_square
        self.present_square = first_square
        self.path = [first_square]

    def update_position(self, new_position: int):
        self.present_square = new_position
        self.path.append(self.present_square)

    def get_position(self):
        return self.present_square

    def clear(self):
        self.present_square = self.first_square
        self.path = [self.first_square]

    def __str__(self):
        return self.name + " has been in " + str(self.path)


class BoardNormalRule(BoardInterface):

    def __init__(self, squares_qtt: int, the_ladders: dict, the_snakes: dict):
        self.squares_qtt = squares_qtt
        self.ladders = the_ladders
        self.snakes = the_snakes

    def move_player(self, player: Player, movements_quantity: int):
        next_square = player.present_square + movements_quantity
        next_square = self.ladders.get(next_square, next_square)
        next_square = self.snakes.get(next_square, next_square)
        player.update_position(next_square)

    def check_board_consistency(self):
        pass


class BoardPlayerImmunity(BoardInterface):

    def __init__(self, squares_qtt: int, the_ladders: dict, the_snakes: dict, player_with_immunity: Player):
        self.squares_qtt = squares_qtt
        self.ladders = the_ladders
        self.snakes = the_snakes
        self.player_with_immunity = player_with_immunity
        self.has_been_taken_on_snake = False

    def move_player(self, player: PlayerInterface, movements_quantity: int):
        next_square = player.get_position() + movements_quantity
        if self.ladders.get(next_square) is not None \
                and (not self.has_been_taken_on_snake or player is not self.player_with_immunity):
            self.has_been_taken_on_snake = True
            next_square = self.ladders.get(next_square)
        next_square = self.snakes.get(next_square, next_square)
        player.update_position(next_square)


class Game:

    def __init__(self, the_board: BoardInterface, players: list):
        """
        :param the_board:
        :param players: the list index is the the order of the player in the game
        """
        self.board = the_board
        self.players = players

    def roll_six_sided_dice(self):
        return random.randint(1, 6)

    def move_player(self, player: PlayerInterface, movements_quantity: int):
        """
        :param player:
        :param movements_quantity:
        :return: true if the informed player wins in the while of executing this move_player
        """
        self.board.move_player(player, movements_quantity)
        return player.present_square >= self.board.squares_qtt

    def play(self) -> PlayerInterface:
        """
        :return: the winner
        """
        while True:
            for player in self.players:
                moves_quantity = self.roll_six_sided_dice()
                if self.move_player(player, moves_quantity):
                    return player

    def restart(self):
        for player in self.players:
            player.clear()


if __name__ == '__main__':
    ladders = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
    snakes = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    board = BoardNormalRule(36, ladders, snakes)
    # print(board.move_player(1, 2))
    player1 = Player('player1', 1)
    player2 = Player('player2', 1)
    game = Game(board, [player1, player2])
    winner = game.play()
    print(winner.name)
    print(player1)
    print(player2)