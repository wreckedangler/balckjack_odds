import random
import matplotlib.pyplot as plt
import multiprocessing
import time


def deal(deck, hand, total, lim):
    while total < lim:
        card = random.choice(deck)
        deck.remove(card)
        hand.append(card)
        if card == 11 and total + card > 21:
            total += 1
        else:
            total += card
    return total


def play_game(lim):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(deck)
    player_hand = []
    dealer_hand = []
    twentyone = 0
    bust = 0
    player_total = deal(deck, player_hand, 0, lim)

    if player_total > 21:
        bust = 1
        return 0, twentyone, bust  # Player busts
    if player_total == 21:
        twentyone = 1

    dealer_total = deal(deck, dealer_hand, 0, player_total)

    if dealer_total > 21 or player_total > dealer_total:
        return 1, twentyone, bust  # Player wins
    return 0, twentyone, bust  # Dealer wins


def multi_process(player_wins_per_draw_limit, player_21s, busts, dealer_wins_per_draw_limit, lim, games, stat):
    with multiprocessing.Pool() as pool:
        results, twentyone, bust = zip(*pool.map(play_game, [lim] * games))
    player_wins = sum(results)
    dealer_wins = games - player_wins
    player_wins_per_draw_limit.append(player_wins)
    dealer_wins_per_draw_limit.append(dealer_wins)
    player_21s.append(sum(twentyone))
    busts.append(sum(bust))
    write_stat(stat, player_wins, lim, games)
    print_stat(player_wins, games, lim)


def single_process(player_wins_per_draw_limit, player_21s, busts, dealer_wins_per_draw_limit, lim, games, stat):
    results, twentyone, bust = zip(*[play_game(lim) for _ in range(games)])
    player_wins = sum(results)
    dealer_wins = games - player_wins
    player_wins_per_draw_limit.append(player_wins)
    dealer_wins_per_draw_limit.append(dealer_wins)
    player_21s.append(sum(twentyone))
    busts.append(sum(bust))
    write_stat(stat, player_wins, lim, games)
    print_stat(player_wins, games, lim)


def print_stat(player_wins, games, lim):
    print(f"Draw-limit: {lim} ¦ Player winrate = {round(player_wins / games * 100, 2)}%")


def write_stat(stat, player_wins, lim, games):
    stat.write(f"Draw-limit: {lim} -> {round(player_wins / games * 100, 2)} % \n")


def get_best_draw_limit(player_wins_per_draw_limit, draw_point_limit):
    best_draw_limit = draw_point_limit[player_wins_per_draw_limit.index(max(player_wins_per_draw_limit))]
    return best_draw_limit


def plot_results(draw_point_limit, player_wins_per_draw_limit, player_21s, busts, dealer_wins_per_draw_limit, games,
                 best_draw_limit):
    plt.figure(figsize=(14, 10))

    # Plot player wins per draw limit
    plt.subplot(2, 2, 1)
    plt.bar(draw_point_limit, player_wins_per_draw_limit, color=['green' if x == best_draw_limit else 'blue'
                                                                 for x in draw_point_limit])
    plt.xlabel('Draw Limit')
    plt.ylabel(f'Player Wins per {games} games')
    plt.title(f'Best Draw Limit')

    # Plot Win rate per draw limit
    plt.subplot(2, 2, 2)
    player_win_rate = [win / games for win in player_wins_per_draw_limit]
    dealer_win_rate = [win / games for win in dealer_wins_per_draw_limit]
    plt.plot(draw_point_limit, dealer_win_rate, label='Dealer', color='red')
    plt.plot(draw_point_limit, player_win_rate, label='Player', color='blue')
    plt.axvline(x=best_draw_limit, color='black', linestyle='--', label='Best Draw Limit')
    plt.xlabel('Draw Limit')
    plt.ylabel('Win Rate')
    plt.title(f'Player / Dealer Win Rate per Draw Limit')
    plt.legend([f'Dealer | min {round(min(dealer_wins_per_draw_limit) / games * 100, 2)}%',
                f'Player | max {round(max(player_wins_per_draw_limit) / games * 100, 2)}%'])

    # Plot players 21s (Blackjacks) and Busts per draw limit
    plt.subplot(2, 2, 3)
    plt.plot(draw_point_limit, player_21s, color='green')
    plt.plot(draw_point_limit, busts, color='red')
    plt.xlabel('Draw Limit')
    plt.ylabel(f'Times per {games} games')
    plt.title(f'21 Points and Busts per Draw Limit')
    plt.legend(['Player 21s', 'Player Busts'])

    # Plot General win rate of all played games
    plt.subplot(2, 2, 4)
    total_player_wins = sum(player_wins_per_draw_limit)
    total_dealer_wins = sum(dealer_wins_per_draw_limit)
    total_games = games * len(draw_point_limit)
    general_player_win_rate = total_player_wins / total_games
    general_dealer_win_rate = total_dealer_wins / total_games
    plt.bar(['Player', 'Dealer'], [general_player_win_rate, general_dealer_win_rate], color=['blue', 'red'])
    plt.ylabel('Win Rate')
    plt.title('General Win Rate of all played Games')

    plt.tight_layout(pad=3.0)
    plt.show()


def main():
    path = "blackjack_stats.txt"
    games = 10000
    draw_point_limit = list(range(5, 21))

    with open(path, "w") as stat:
        stat.write(f"Blackjack win odds for player\n\n")
        player_wins_per_draw_limit = []
        player_21s = []
        busts = []
        dealer_wins_per_draw_limit = []
        start = time.time()
        for lim in draw_point_limit:
            if games > 80000:
                multi_process(player_wins_per_draw_limit, player_21s, busts, dealer_wins_per_draw_limit, lim, games, stat)
            else:
                single_process(player_wins_per_draw_limit, player_21s, busts, dealer_wins_per_draw_limit, lim, games, stat)
        end = time.time()
        stat.write(f"\nTotal Games played: {games * len(draw_point_limit)}\n")
        stat.write(f"Time taken: {round(end - start, 3)} seconds\n")
    print(f"Total Games played: {games * len(draw_point_limit)} ")
    print(f"Time taken: {round(end - start, 3)} seconds")
    best_limit = get_best_draw_limit(player_wins_per_draw_limit, draw_point_limit)
    plot_results(draw_point_limit, player_wins_per_draw_limit, player_21s, busts, dealer_wins_per_draw_limit, games,
                 best_limit)


if __name__ == "__main__":
    main()
