import random


class Board:

    def __init__(self, squares_qtt: int, the_ladders: dict, the_snakes: dict):
        self.squares_qtt = squares_qtt
        self.ladders = the_ladders
        self.snakes = the_snakes

    def movement(self, present_square: int, movements_quantity: int):
        next_square = present_square + movements_quantity
        next_square = self.ladders.get(next_square, next_square)
        return self.snakes.get(next_square, next_square)

    def check_board_consistency(self):
        pass


class Player:

    def __init__(self, name, first_square):
        self.name = name
        # self.first_square = first_square
        self.present_square = first_square
        self.path = [first_square]

    def update_position(self, new_position: int):
        self.present_square = new_position
        self.path.append(self.present_square)

    def __str__(self):
        return self.name + " has been in " + str(self.path)


class Game:

    def __init__(self, the_board: Board, players: list):
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
        :return: true if the informed player wins in the while of executing this movement
        """
        player.update_position(self.board.movement(player.present_square, movements_quantity))
        return player.present_square >= self.board.squares_qtt

    def play(self) -> Player:
        """
        :return: the winner
        """
        while True:
            for player in self.players:
                moves_quantity = self.roll_six_sided_dice()
                if self.move_player(player, moves_quantity):
                    return player


class BoardPlayer2Immunity(Board):

    def movement(self, present_square: int, movements_quantity: int):
        next_square = present_square + movements_quantity
        next_square = self.ladders.get(next_square, next_square)
        return self.snakes.get(next_square, next_square)


if __name__ == '__main__':
    ladders = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
    snakes = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    board = Board(36, ladders, snakes)
    # print(board.movement(1, 2))
    player1 = Player('player1', 1)
    player2 = Player('player2', 1)
    game = Game(board, [player1, player2])
    winner = game.play()
    print(winner.name)
    print(player1)
    print(player2)