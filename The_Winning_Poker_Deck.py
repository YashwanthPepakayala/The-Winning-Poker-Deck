"""
The Winning Poker Deck 🃏
=========================
A Python-based program to determine the winner in a game of Poker. It evaluates players' hands, 
ranks them based on Poker rules, and resolves ties using an intelligent comparison algorithm.

Features:
- Supports standard Poker hand rankings: Royal Flush, Straight Flush, etc.
- Handles tie-breaking scenarios with advanced logic.
- Accepts custom player names and card inputs.

Author: Yashwanth Pepakayala
License: MIT License
"""

from collections import Counter

class Poker:
    """
    A class to evaluate Poker hands and determine the winner.

    Methods:
    --------
    pokerwinner(playersCards: dict) -> int
        Determines the winner based on Poker hand rankings and tie-breaking logic.
    to_numerics(scards: list) -> list
        Converts card ranks to numerical values for easier comparison.
    counting(scards: list) -> Counter
        Counts occurrences of each card rank in the player's hand.
    is_royalflush(suits: dict, numerics: list) -> bool
        Checks if a hand is a Royal Flush.
    is_Straightflush(suits: dict, numerics: list) -> bool
        Checks if a hand is a Straight Flush.
    is_4oak(counter: Counter) -> bool
        Checks if a hand is Four of a Kind.
    is_fullhouse(counter: Counter) -> bool
        Checks if a hand is a Full House.
    is_flush(suits: dict) -> bool
        Checks if a hand is a Flush.
    is_Straight(numerics: list) -> bool
        Checks if a hand is a Straight.
    is_3oak(counter: Counter) -> bool
        Checks if a hand is Three of a Kind.
    is_2p(counter: Counter) -> bool
        Checks if a hand is Two Pair.
    is_1p(counter: Counter) -> bool
        Checks if a hand is One Pair.
    tiebreak(winners: list, player_numerics: dict) -> int
        Resolves ties by comparing players' hands numerically.
    """

    def pokerwinner(self, playersCards):
        """
        Determines the winner among players by evaluating Poker hands.

        Parameters:
        ----------
        playersCards : dict
            A dictionary where keys are player indices, and values are tuples of player name 
            and their respective card hands.

        Returns:
        -------
        int
            The index of the winning player. If no winner is found, returns -1.
        """
        results = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
        player_numerics = {}

        for ind, player_data in playersCards.items():
            name, cards = player_data
            suits = {'H': 0, 'S': 0, 'C': 0, 'D': 0}
            for card in cards:
                suits[card[-1]] += 1

            scards = [i[:-1] for i in cards]
            numerics = self.to_numerics(scards)
            player_numerics[ind] = numerics
            counter = self.counting(scards)

            # Check poker hand categories
            if self.is_royalflush(suits, numerics):
                results[1].append(ind)
            elif self.is_Straightflush(suits, numerics):
                results[2].append(ind)
            elif self.is_4oak(counter):
                results[3].append(ind)
            elif self.is_fullhouse(counter):
                results[4].append(ind)
            elif self.is_flush(suits):
                results[5].append(ind)
            elif self.is_Straight(numerics):
                results[6].append(ind)
            elif self.is_3oak(counter):
                results[7].append(ind)
            elif self.is_2p(counter):
                results[8].append(ind)
            elif self.is_1p(counter):
                results[9].append(ind)
            else:
                results[10].append(ind)

        # Determine the winner by ranking the hand categories
        for rank in range(1, 11):
            if results[rank]:
                winners = results[rank]
                if len(winners) == 1:
                    return winners[0]
                else:
                    return self.tiebreak(winners, player_numerics)

        return -1

    def to_numerics(self, scards):
        """
        Converts card ranks to numerical values for evaluation.

        Parameters:
        ----------
        scards : list
            A list of string card ranks (e.g., ['10', 'J', 'Q']).

        Returns:
        -------
        list
            A sorted list of card ranks converted to numerical values.
        """
        rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                    '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        numerics = [rank_map[rank] for rank in scards]

        if 14 in numerics and 2 in numerics:
            numerics = [1 if rank == 14 else rank for rank in numerics]

        numerics.sort(reverse=True)
        return numerics

    def counting(self, scards):
        """
        Counts occurrences of each card rank.

        Parameters:
        ----------
        scards : list
            A list of string card ranks.

        Returns:
        -------
        Counter
            A Counter object containing counts of each card rank.
        """
        return Counter(scards)

    def is_royalflush(self, suits, numerics):
        return max(suits.values()) == 5 and numerics == [14, 13, 12, 11, 10]

    def is_Straightflush(self, suits, numerics):
        return max(suits.values()) == 5 and len(set(numerics)) == 5 and numerics[0] - numerics[-1] == 4

    def is_4oak(self, counter):
        return 4 in counter.values()

    def is_fullhouse(self, counter):
        return 3 in counter.values() and 2 in counter.values()

    def is_flush(self, suits):
        return max(suits.values()) == 5

    def is_Straight(self, numerics):
        return len(set(numerics)) == 5 and numerics[0] - numerics[-1] == 4

    def is_3oak(self, counter):
        return 3 in counter.values()

    def is_2p(self, counter):
        return sum(1 for count in counter.values() if count == 2) == 2

    def is_1p(self, counter):
        return sum(1 for count in counter.values() if count == 2) == 1

    def tiebreak(self, winners, player_numerics):
        """
        Resolves ties by comparing players' numerical hands.

        Parameters:
        ----------
        winners : list
            A list of player indices who are tied.
        player_numerics : dict
            A dictionary mapping player indices to their numerical hands.

        Returns:
        -------
        int
            The index of the player with the best hand.
        """
        best_player = winners[0]
        best_hand = player_numerics[best_player]

        for player in winners[1:]:
            for card1, card2 in zip(player_numerics[player], best_hand):
                if card1 > card2:
                    best_player = player
                    best_hand = player_numerics[player]
                    break
                elif card1 < card2:
                    break

        return best_player


def get_player_cards(num_players):
    """
    Collects player names and card inputs from the user.

    Parameters:
    ----------
    num_players : int
        The number of players in the game.

    Returns:
    -------
    dict
        A dictionary where keys are player indices, and values are tuples of player name and card hands.
    """
    playersCards = {}
    for i in range(1, num_players + 1):
        name = input(f"Enter the name of Player {i}: ")
        cards = input(f"Enter cards for {name} (separate by space): ").split()
        playersCards[i] = (name, cards)
    return playersCards


def main():
    """
    Main function to run the Poker Winner Evaluator.
    """
    print("Welcome to Poker Winner Evaluator! 🃏")
    num_players = int(input("Enter the number of players: "))
    playersCards = get_player_cards(num_players)

    poker = Poker()
    winner_index = poker.pokerwinner(playersCards)
    if winner_index == -1:
        print("No winner!")
    else:
        winner_name = playersCards[winner_index][0]
        print(f"The winner is {winner_name}!")


if __name__ == "__main__":
    main()
