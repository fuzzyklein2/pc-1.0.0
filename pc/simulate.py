import eval7
import random

def simulate_win_probability(hero_hand_strs, board_strs, num_opponents, num_simulations=10000):
    hero_hand = [eval7.Card(card) for card in hero_hand_strs]
    board = [eval7.Card(card) for card in board_strs]
    
    wins = 0
    ties = 0

    for _ in range(num_simulations):
        # Build and shuffle deck
        deck = eval7.Deck()
        for card in hero_hand + board:
            deck.cards.remove(card)
        deck.shuffle()

        # Deal opponents
        opponent_hands = []
        for _ in range(num_opponents):
            opponent_hands.append([deck.deal(1)[0], deck.deal(1)[0]])

        # Complete the board if needed
        remaining_board_cards = 5 - len(board)
        sim_board = board + deck.peek(remaining_board_cards)

        # Evaluate hero hand
        hero_score = eval7.evaluate(hero_hand + sim_board)

        # Evaluate opponents
        best_opponent_score = -1
        tie_count = 0
        for opp_hand in opponent_hands:
            opp_score = eval7.evaluate(opp_hand + sim_board)
            if opp_score > hero_score:
                best_opponent_score = max(best_opponent_score, opp_score)
            elif opp_score == hero_score:
                tie_count += 1

        # Win/tie/loss logic
        if best_opponent_score > hero_score:
            continue  # loss
        elif tie_count > 0:
            ties += 1
        else:
            wins += 1

    total = num_simulations
    print(f"Hero wins: {wins / total:.4f} ({wins} of {total})")
    print(f"Ties:      {ties / total:.4f} ({ties} of {total})")
    print(f"Losses:    {(total - wins - ties) / total:.4f} ({total - wins - ties} of {total})")
