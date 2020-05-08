import sys

from board_game import BoardNormalRule, BoardPlayerImmunity, Player, Game, BoardInterface, BoardFiftyPercentRule


def get_board_normal_rule():
    ladders = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
    snakes = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    return BoardNormalRule(36, ladders, snakes)


# Question 1 #
def answering_question1(simulations_run):
    print("Question1: In a two person game, what is the probability that the player who starts the game wins?")
    board = get_board_normal_rule()
    starting_player_victories_frequency \
        = simulate_two_players_match(board, Player('player1', 1), Player('player2', 1), simulations_run)
    print('The probability is about ' + str(round(starting_player_victories_frequency, 3)))


def simulate_two_players_match(board: BoardInterface, player1: Player, player2: Player, simulations_run: int):
    """
    :param board:
    :param player1: the player who start all the matches
    :param player2:
    :param simulations_run:
    :return: The relative frequency of starting player victories
    """
    starting_player_victories_amount = 0
    for run in range(simulations_run):
        game = Game(board.copy(), [player1.copy(), player2.copy()])
        winner = game.play()
        if winner.name == player1.name:
            starting_player_victories_amount += 1
    return starting_player_victories_amount / simulations_run


# Question 2 #
def answering_question2(simulations_run):
    print("Question 2: On average, how many snakes are landed on in each game?")
    total_amount_lands_on_snake = 0
    for run in range(simulations_run):
        board = get_board_normal_rule()
        game = Game(board, [Player('player1', 1), Player('player2', 1)])
        game.play()
        total_amount_lands_on_snake += count_board_objects_use(board.get_snakes_used())
    average = total_amount_lands_on_snake / simulations_run
    print('The average is ' + str(round(average, 2)))


def count_board_objects_use(used_object_dictionary: dict):
    total_quantity = 0
    for object_key, quantity_used in used_object_dictionary.items():
        total_quantity += quantity_used
    return total_quantity


# Question 3#
def answering_question3(simulations_run):
    print("Question3: If each time a player landed on a ladder and there was only a 50% chance they could "
          "take it, what is the average number of rolls needed to complete a game? ")
    count_sampled_matches_polls = 0
    ladders = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
    snakes = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    for run in range(simulations_run):
        board = BoardFiftyPercentRule(36, ladders, snakes)
        players = [Player('player1', 1), Player('player2', 1)]
        game = Game(board, players)
        game.play()
        for player in game.get_players():
            count_sampled_matches_polls += player.get_rolls_quantity()
    print('The average is ' + str(round(count_sampled_matches_polls / simulations_run, 1)))


# Question 3 Wrong#
def answering_question3_wrong(simulations_run):
    print("Question3: If each time a player landed on a ladder and there was only a 50% chance they could "
          "take it, what is the average number of rolls needed to complete a game? ")
    ladders_frequencies = estimate_ladders_use_relative_frequencies(get_board_normal_rule(), Player("player1", 1),
                                                                    Player("player2", 1), simulations_run)
    ladder_keys_closest_fifty = get_keys_with_probability_closest_to_reference(ladders_frequencies, 0.5)
    print("The ladder with relative frequency closest to 50% and its(their) percent value is(are)",
          [(ladder_keys_closest_fifty, round(100 * ladders_frequencies[key], 1)) for key in ladder_keys_closest_fifty])
    count_sampled_matches = 0
    count_sampled_matches_polls = 0
    for run in range(simulations_run):
        board = get_board_normal_rule()
        players = [Player('player1', 1), Player('player2', 1)]
        game = Game(board, players)
        game.play()
        if check_contain_key(board.get_ladders_used(), ladder_keys_closest_fifty):  # is not None:
            count_sampled_matches += 1
            for player in game.get_players():
                count_sampled_matches_polls += player.get_rolls_quantity()
    print('The average is ' + str(round(count_sampled_matches_polls / count_sampled_matches, 1)))


def check_contain_key(dictionary: dict, keys):
    for key in keys:
        if dictionary.get(key) is not None:
            return True
    return False


def estimate_ladders_use_relative_frequencies(board: BoardNormalRule, player1: Player, player2: Player,
                                              simulations_run: int):
    """
    Estimate relative frequencies in a game with the normal rule board and two players.
    A ladder that is used more than one time is count only once
    :param player1: player who start
    :param player2:
    :param board:
    :param simulations_run:
    :return: The dictionary of relative frequencies of each ladder where a lands on has happened
    """
    ladders_use = {}
    for run in range(simulations_run):
        new_board = board.copy()
        game = Game(new_board, [player1.copy(), player2.copy()])
        game.play()
        for ladder, occurrence in new_board.get_ladders_used().items():
            if occurrence > 0:
                ladders_use[ladder] = ladders_use.get(ladder, 0) + 1
    for ladder, occurrence in ladders_use.items():
        ladders_use[ladder] = occurrence / simulations_run
    return ladders_use


# Question 4 #
def answering_question4(simulations_run):
    print("Question 4: Starting with the base game, you decide you want the game to have approximately fair odds."
          " You do this by changing the square that Player 2 starts on. Which square for Player 2’s "
          "start position gives the closest to equal odds for both players? ")
    board = get_board_normal_rule()
    start_position_and_player1_wins_frequencies = \
        simulate_player2_starting_in_all_board_squares(board, 'player2', simulations_run)
    max_fair_frequency_positions = \
        get_keys_with_probability_closest_to_reference(start_position_and_player1_wins_frequencies, 0.5)
    print("The max fair position(s) and its(their) relative frequencies is(are)",
          [(str(max_frequency_position), round(start_position_and_player1_wins_frequencies[max_frequency_position], 2))
           for max_frequency_position in max_fair_frequency_positions])


def simulate_player2_starting_in_all_board_squares(board: BoardInterface, player2_name, simulations_run):
    """
    Simulations for player2 starting in each position of the board while player1 aways starts in position 1
    If the player 2 start in a square where there is  a ladder or a snake, than the player will not use them.
    :param board:
    :param player2_name:
    :param simulations_run:
    :return: Dictionary from player2 start positions in the board to the achieved relative frequencies of player 1 wins
    """
    start_position_to_player1_frequencies = {}
    for start_square in range(1, board.squares_qtt + 1):
        player2 = Player(player2_name, start_square)
        start_position_to_player1_frequencies[start_square] = \
            simulate_two_players_match(board.copy(), Player('player1', 1), player2, simulations_run)
    return start_position_to_player1_frequencies


def get_keys_with_probability_closest_to_reference(start_position_and_probability: dict, reference: float):
    min_difference = sys.maxsize
    positions_most_fair_odds = []
    for start_position, frequency in start_position_and_probability.items():
        difference = abs(frequency - reference)
        if difference < min_difference:
            positions_most_fair_odds.clear()
            min_difference = difference
            positions_most_fair_odds.append(start_position)
        elif difference == min_difference:
            positions_most_fair_odds.append(start_position)
    return positions_most_fair_odds


# Question 5 #
def answering_question5(simulations_run):
    print("Question 5: In a different attempt to change the odds of the game, instead of starting Player 2 on a "
          "different square, you decide to give Player 2 immunity to the first snake that they land on. What is "
          "the approximate probability that Player 1 wins now? ")
    ladders = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
    snakes = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    immune_player_name = "player2"
    board = BoardPlayerImmunity(36, ladders, snakes, immune_player_name)
    starting_player_victories_frequency \
        = simulate_two_players_match(board, Player('player1', 1), Player('player2', 1), simulations_run)
    print('The probability is about ' + str(round(starting_player_victories_frequency, 4)))


if __name__ == '__main__':
    # answering_question1(10000)
    # answering_question2(10000)
    answering_question3(10000)
    # answering_question4(10000)
    # answering_question5(10000)
