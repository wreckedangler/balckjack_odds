import random
import matplotlib.pyplot as plt


# Deal function to deal cards to player and dealer
def deal(deck, hand, total, lim):
    while total < lim:
        card = random.choice(deck)
        deck.remove(card)
        hand.append(card)
        if card == 11 and total + card > 21:
            total += 1
        else:
            total += card
    return total, hand


# Function to play a single game of blackjack
def play_game(deck, lim):
    player_hand = []
    dealer_hand = []
    player_total, _ = deal(deck, player_hand, 0, lim)

    # If the player doesn't bust, the dealer plays
    if player_total <= 21:
        dealer_total, _ = deal(deck, dealer_hand, 0, 17)
    else:
        return 0
    return 1 if player_total <= 21 and player_total > dealer_total else 0


# Function to simulate multiple games of blackjack and plot the results
def main():
    path = "C:\\Users\\raphi\\PycharmProjects\\pythonProject\\SchoolExample\\Blackjack\\stats"
    games = 100000
    with open(path + ".txt", "w") as stat:
        stat.write(f"Blackjack player-wins out of {games} games.\n")
        draw_point_limit = list(range(5, 22))
        player_wins_per_draw_limit = []
        for lim in draw_point_limit:
            player_wins = sum(play_game(deck := [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 6, lim)
                              for _ in range(games))
            dealer_wins = games - player_wins
            # print(f"Draw-limit: {lim} ¦ Player winrate = {round(player_wins / games * 100, 2)}%")
            stat.write(f"Draw-limit: {lim} points = {player_wins}\n")
            player_wins_per_draw_limit.append(player_wins)
            print(player_wins, dealer_wins)
    plot_results(draw_point_limit, player_wins_per_draw_limit)


# Function to plot the results of the simulation
def plot_results(draw_point_limit, player_wins_per_draw_limit):
    plt.plot(draw_point_limit, player_wins_per_draw_limit)
    plt.xlabel('Draw Limit')
    plt.ylabel('Player Wins')
    plt.title('Player Wins per Draw Limit')
    plt.show()


if __name__ == "__main__":
    main()