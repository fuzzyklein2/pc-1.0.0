import eval7
import random

def compute_preflop_equity(hand_str, num_opponents=1, num_trials=100000):
    """
    Estimate preflop equity using Monte Carlo simulation.
    
    Parameters:
        hand_str (str): Your 2-card hand, e.g. "AsKs", "7h7d", "Jc2d"
        num_opponents (int): Number of opponents (1-9)
        num_trials (int): Number of simulations to run (default: 100,000)
    
    Returns:
        float: Estimated win percentage (0–100)
    """
    assert len(hand_str) == 4, "Hand must be 4 characters, e.g. 'AsKs'"
    assert 1 <= num_opponents <= 9, "Opponents must be between 1 and 9"

    hero_hand = [eval7.Card(hand_str[:2]), eval7.Card(hand_str[2:])]
    wins = 0
    ties = 0

    for _ in range(num_trials):
        deck = eval7.Deck()
        for card in hero_hand:
            deck.cards.remove(card)

        # Deal opponent hands
        opponent_hands = []
        for _ in range(num_opponents):
            opp_hand = [deck.deal(), deck.deal()]
            opponent_hands.append(opp_hand)

        # Deal 5-card board
        board = [deck.deal() for _ in range(5)]

        hero_score = eval7.evaluate(hero_hand + board)
        opp_scores = [eval7.evaluate(h + board) for h in opponent_hands]

        all_scores = opp_scores + [hero_score]
        max_score = max(all_scores)

        if hero_score == max_score:
            if all_scores.count(max_score) == 1:
                wins += 1
            else:
                ties += 1

    equity = 100 * (wins + ties / 2) / num_trials
    return round(equity, 4)
