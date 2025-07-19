
# Monte Carlo Simulations for Poker

## What is a Monte Carlo Simulation?

Monte Carlo simulations are a **computational method** used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of **random variables**.

They are used in a wide range of fields, including:
- **Finance**
- **Physics**
- **Engineering**
- **Games**
- **Optimization and AI**

### Core Concept
1. Define a model with some random elements.
2. Generate random inputs.
3. Run many simulations.
4. Aggregate results to analyze outcomes and probabilities.

### Example: Estimating π

```python
import random

def estimate_pi(num_samples):
    inside_circle = 0
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            inside_circle += 1
    return 4 * inside_circle / num_samples
```

### Why Use Monte Carlo Simulations?

- Handle uncertainty
- Approximate solutions
- Parallel-friendly

### Limitations

- Slow convergence
- Computationally expensive
- Quality depends on randomness

---

## Applying Monte Carlo to Poker

User wants to implement simulations to estimate the probability that a given hand will win in Texas Hold’em.

### Using eval7 to Compare Hands

```python
import eval7

hero_hand = [eval7.Card('A♠'), eval7.Card('A♣')]
villain_hand = [eval7.Card('K♦'), eval7.Card('K♣')]
board = [eval7.Card('2♦'), eval7.Card('7♠'), eval7.Card('J♣'),
         eval7.Card('9♣'), eval7.Card('3♥')]

hero_score = eval7.evaluate(hero_hand + board)
villain_score = eval7.evaluate(villain_hand + board)

if hero_score > villain_score:
    print("Hero wins!")
elif hero_score < villain_score:
    print("Villain wins!")
else:
    print("It's a tie!")
```

### Full Monte Carlo Simulation with eval7

```python
import eval7
import random

def simulate_win_probability(hero_hand_strs, board_strs, num_opponents, num_simulations=10000):
    hero_hand = [eval7.Card(card) for card in hero_hand_strs]
    board = [eval7.Card(card) for card in board_strs]

    wins = 0
    ties = 0

    for _ in range(num_simulations):
        deck = eval7.Deck()
        for card in hero_hand + board:
            deck.cards.remove(card)
        deck.shuffle()

        opponent_hands = []
        for _ in range(num_opponents):
            opponent_hands.append([deck.deal(1)[0], deck.deal(1)[0]])

        remaining_board_cards = 5 - len(board)
        sim_board = board + deck.peek(remaining_board_cards)

        hero_score = eval7.evaluate(hero_hand + sim_board)

        best_opponent_score = -1
        tie_count = 0
        for opp_hand in opponent_hands:
            opp_score = eval7.evaluate(opp_hand + sim_board)
            if opp_score > hero_score:
                best_opponent_score = max(best_opponent_score, opp_score)
            elif opp_score == hero_score:
                tie_count += 1

        if best_opponent_score > hero_score:
            continue
        elif tie_count > 0:
            ties += 1
        else:
            wins += 1

    total = num_simulations
    print(f"Hero wins: {wins / total:.4f} ({wins} of {total})")
    print(f"Ties:      {ties / total:.4f} ({ties} of {total})")
    print(f"Losses:    {(total - wins - ties) / total:.4f} ({total - wins - ties} of {total})")
```

### Example Usage

```python
simulate_win_probability(
    hero_hand_strs=['As', 'Ac'],
    board_strs=['Kd', 'Qs', '2h'],
    num_opponents=2,
    num_simulations=10000
)
```
