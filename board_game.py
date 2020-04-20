import random


class Player:

    def __init__(self, name, first_position: int):
        self.name = name
        self.first_position = first_position
        self.present_position = first_position
        self.path = [first_position]

    def update_position(self, new_position: int):
        self.present_position = new_position
        self.path.append(self.present_position)

    def get_present_position(self):
        return self.present_position

    def get_first_position(self):
        return self.first_position

    def get_rolls_quantity(self):
        return len(self.path) - 1

    def copy(self):
        return Player(self.name, self.first_position)

    def __str__(self):
        return self.name + " has been in " + str(self.path)


class BoardInterface:
    def move_player(self, player: Player, movements_quantity: int):
        """
           :param player: the player executing the movement
           :param movements_quantity:
           :return: the next square where the player go
        """
        pass

    def get_squares_quantity(self):
        """
        :return: the quantity of squares in the board
        """
        pass

    def copy(self):
        """
        :return: A copy of the board
        """
        pass


class BoardNormalRule(BoardInterface):

    def __init__(self, squares_qtt: int, the_ladders: dict, the_snakes: dict):
        # constants
        self.squares_qtt = squares_qtt
        self.ladders = the_ladders
        self.snakes = the_snakes
        # variables
        self.ladders_use = {}
        self.snakes_use = {}

    def move_player(self, player: Player, movements_quantity: int):
        next_square = player.present_position + movements_quantity
        if self.snakes.get(next_square) is not None:
            snake_key = str(next_square) + "-" + str(self.snakes.get(next_square))
            self.snakes_use[snake_key] = self.snakes_use.get(snake_key, 0) + 1
            next_square = self.snakes.get(next_square)
        if self.ladders.get(next_square) is not None:
            ladder_key = str(next_square) + "-" + str(self.ladders.get(next_square))
            self.ladders_use[ladder_key] = self.ladders_use.get(ladder_key, 0) + 1
            next_square = self.ladders.get(next_square)
        player.update_position(next_square)

    def get_squares_quantity(self):
        return self.squares_qtt

    def get_ladders_used(self):
        return self.ladders_use

    def get_snakes_used(self):
        return self.snakes_use

    def copy(self):
        return BoardNormalRule(self.squares_qtt, self.ladders, self.snakes)


class BoardPlayerImmunity(BoardInterface):

    def __init__(self, squares_qtt: int, the_ladders: dict, the_snakes: dict, immune_player_name):
        self.squares_qtt = squares_qtt
        self.ladders = the_ladders
        self.snakes = the_snakes
        self.immune_player_name = immune_player_name
        # var
        self.is_still_immune = True

    def move_player(self, player: Player, movements_quantity: int):
        next_square = player.get_present_position() + movements_quantity
        next_square = self.ladders.get(next_square, next_square)
        if self.snakes.get(next_square) is not None:
            if player.name == self.immune_player_name and self.is_still_immune:
                self.is_still_immune = False
            else:
                next_square = self.snakes.get(next_square)
        player.update_position(next_square)

    def get_squares_quantity(self):
        return self.squares_qtt

    def copy(self):
        return BoardPlayerImmunity(self.squares_qtt, self.ladders, self.snakes, self.immune_player_name)


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

    def move_player(self, player: Player, movements_quantity: int):
        """
        :param player:
        :param movements_quantity:
        :return: true if the informed player wins in the while of executing this move_player
        """
        self.board.move_player(player, movements_quantity)
        return player.present_position >= self.board.squares_qtt

    def play(self) -> Player:
        """
        :return: the winner
        """
        while True:
            for player in self.players:
                moves_quantity = self.roll_six_sided_dice()
                if self.move_player(player, moves_quantity):
                    return player

    def get_players(self):
        return self.players


if __name__ == '__main__':
    ladders = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
    snakes = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    board = BoardNormalRule(36, ladders, snakes)
    player1 = Player('player1', 1)
    player2 = Player('player2', 1)
    game = Game(board, [player1, player2])
    winner = game.play()
    print(winner.name)
    print(player1)
    print(player2)
    dice_frequencies = {}
    for i in range(1000000):
        value = game.roll_six_sided_dice()
        dice_frequencies[value] = dice_frequencies.get(value, 0) + 1
    print(dice_frequencies)
