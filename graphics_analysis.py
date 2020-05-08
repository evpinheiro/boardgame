from board_game import BoardNormalRule, BoardPlayerImmunity, Player, Game, BoardInterface
from questions_analysis import *
import matplotlib.pyplot as plt


def graph_studying_conditioning_question3(simulations_run):
    ladders_frequencies = estimate_ladders_use_relative_frequencies(get_board_normal_rule(), Player("player1", 1),
                                                                    Player("player2", 1), simulations_run)
    print(ladders_frequencies)
    x, y = zip(*sorted(ladders_frequencies.items()))
    fig, ax = plt.subplots()
    ax.bar(x, y)
    plt.axhline(y=0.5, color='r', linestyle='-')
    plt.show()


def graph_studying_question3(simulations_run):
    ladders_frequencies = estimate_ladders_use_relative_frequencies(get_board_normal_rule(), Player("player1", 1),
                                                                    Player("player2", 1), simulations_run)
    ladder_keys_closest_fifty = get_keys_with_probability_closest_to_reference(ladders_frequencies, 0.5)
    print("The ladder with relative frequency closest to 50% and its(their) percent value is(are)",
          [(ladder_keys_closest_fifty, round(100 * ladders_frequencies[key], 1)) for key in ladder_keys_closest_fifty])
    count_sampled_matches = 0
    count_sampled_matches_polls = 0
    run_rolls_quantity = {}
    selected_match = {}
    for run in range(simulations_run):
        board = get_board_normal_rule()
        players = [Player('player1', 1), Player('player2', 1)]
        game = Game(board, players)
        game.play()
        for player in game.get_players():
            run_rolls_quantity[run] = run_rolls_quantity.get(run, 0) + player.get_rolls_quantity()
        if run_rolls_quantity[run] == 5:
            for player in game.get_players():
                print(player.name, player.path)
        if check_contain_key(board.get_ladders_used(), ladder_keys_closest_fifty):
            count_sampled_matches += 1
            count_sampled_matches_polls += run_rolls_quantity[run]
            selected_match[run] = run_rolls_quantity[run]
    x, y = zip(*sorted(run_rolls_quantity.items()))
    print(min(y))
    x1, y1 = zip(*sorted(selected_match.items()))
    print(min(y1))
    plt.plot(x, y, '*', x1, y1, '.')
    plt.axhline(y=sum(y)/len(y), color='r', linestyle='-')
    # fig, ax = plt.subplots()
    # ax.bar(x, y)
    plt.show()


if __name__ == '__main__':
    graph_studying_conditioning_question3(10000)
    graph_studying_question3(10000)
