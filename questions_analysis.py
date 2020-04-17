import sys

from board_game import Board, Player, Game


def get_board():
    ladders = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
    snakes = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    return Board(36, ladders, snakes)


# Question 1 #
def answer_question1(simulations_run):
    question = "In a two person game, what is the probability that the player who starts the game wins?"
    starting_player_victories_frequency = simulate_two_players_match(simulations_run)
    print(question)
    print('The probability is about ' + str(starting_player_victories_frequency))


def simulate_two_players_match(simulations_run: int, player2_start_square=1):
    board = get_board()
    starting_player = 'player1'
    starting_player_victories_amount = 0
    for count in range(simulations_run):
        game = Game(board, [Player(starting_player, 1), Player('player2', player2_start_square)])
        winner = game.play()
        if winner.name == starting_player:
            starting_player_victories_amount += 1
    return starting_player_victories_amount / simulations_run


# Question 2 #
def answering_question2(simulations_run):
    question = "On average, how many snakes are landed on in each game?"
    board = get_board()
    total_amount_lands_on_snake = 0
    for run in range(simulations_run):
        players = [Player('player1', 1), Player('player2', 1)]
        game = Game(board, players)
        game.play()
        total_amount_lands_on_snake += count_lands_on_snake(players, None)
    print(question)
    print('The average is ' + str(total_amount_lands_on_snake / simulations_run))


def count_lands_on_snake(players):
    quantity = 0
    for player in players:
        for i in range(len(player.path)-1):
            # this only works if the snakes always late the player
            if player.path[i] > player.path[i+1]:
                quantity += 1
    return quantity


# Question 3 #
def answering_question3(simulations_run):
    question = "If each time a player landed on a ladder and there was only a 50% chance they could take it, " \
               "what is the average number of rolls needed to complete a game? "
    board = get_board()
    for run in range(simulations_run):
        players = [Player('player1', 1), Player('player2', 1)]
        game = Game(board, players)
        game.play()
    print(question)
    # print('The average is ' + str(total_amount_lands_on_snake / simulations_run))


# Question 4 #
def answering_question4(simulations_run):
    question = "Starting with the base game, you decide you want the game to have approximately fair odds. You do " \
               "this by changing the square that Player 2 starts on. Which square for Player 2’s start position gives " \
               "the closest to equal odds for both players? "
    board = get_board()
    start_position_and_frequencies = {}
    for player2_start_square in range(1, board.squares_qtt+1):
        start_position_and_frequencies[player2_start_square] = \
            simulate_two_players_match(simulations_run, player2_start_square)
    print(question)
    print(start_position_and_frequencies)
    max_frequency_positions = get_max_fair_positions(start_position_and_frequencies)
    print([(str(max_frequency_position), start_position_and_frequencies[max_frequency_position])
           for max_frequency_position in max_frequency_positions])


def get_max_fair_positions(start_position_and_probability: dict):
    min_difference = sys.maxsize
    positions_most_fair_odds = []
    for start_position, frequency in start_position_and_probability.items():
        difference = abs(frequency - 0.5)
        if difference < min_difference:
            positions_most_fair_odds.clear()
            min_difference = difference
            positions_most_fair_odds.append(start_position)
        elif difference == min_difference:
            positions_most_fair_odds.append(start_position)

    return positions_most_fair_odds


# Question 5 #
def answering_question5(simulations_run):
    question = "In a different attempt to change the odds of the game, instead of starting Player 2 on a different " \
               "square, you decide to give Player 2 immunity to the first snake that they land on. What is the " \
               "approximate probability that Player 1 wins now? "
    starting_player_victories_frequency = simulate_two_players_match(simulations_run)
    print(question)
    print('The probability is about ' + str(starting_player_victories_frequency))


if __name__ == '__main__':
    answer_question1(10000)
    # answering_question2(10000)
    # answering_question3(10000)
    # answering_question4(10000)
    answering_question5(10000)
