$E = mc^2$
# Estimating Fold-Inducing Bet Size in Texas Hold'em

## Theory

> I'm playing a hand of Texas Holdem. Throughout the hand, there is some probability that my hand will win. Can 1 - p be assumed to be the probability that I will lose, and therefore the probability that one of my opponents will win?

**Answer:**  
Yes — in theory, your reasoning is correct:

If \( p \) is the probability that **you** will win a hand of Texas Hold'em, then  
\( 1 - p \) is the probability that **you will not win**.

### ✅ When This Holds True
This works cleanly when:
- There are only two possible outcomes: you win or someone else wins.
- There is no chance of a tie.
- You’re using this estimate for **approximate, strategic** betting decisions.

### ⚠️ When You Need to Adjust
- **Ties:** In reality, hands can tie. Then:
  $$
  \text{Tie Probability (T)} + \text{Loss Probability (L)} = 1 - \text{Win Probability (W)}
  $$
- **Multiple Opponents:** “1 - p” includes all possible combinations of other players beating or tying you.

---

## Strategic Application: Inducing Folds

> I don't care about precision or ties or other little details. An approximate value should suffice. The object is to determine what bet will cause my opponent(s) to be more likely to fold than anything else, e.g. the smallest bet that will cause the pot odds to be less than the odds against them winning.

### 🔢 Goal
Find the **smallest bet** \( B \) that makes it **unprofitable** for your opponent to call.

### ✅ Pot Odds Formula
$$
\text{Pot Odds} = \frac{\text{Call Amount}}{\text{Pot Size After Call}}
$$

To discourage calling, make sure:
$$
\text{Pot Odds} > p
$$

Which implies:
$$
\frac{B}{P + B} > p
$$

Where:
- \( B \) = your bet
- \( P \) = pot size
- \( p \) = opponent’s win probability

Solve for \( B \):
$$
B > \frac{p}{1 - p} \cdot P
$$

---

### 🧮 Example

Pot = \$100  
Estimated opponent win probability = 20% or 0.20

$$
B > \frac{0.20}{1 - 0.20} \cdot 100 = \frac{0.20}{0.80} \cdot 100 = 25
$$

So a **\$25+ bet** discourages calling from an opponent with a 20% chance to win.

---

### 💡 Final Formula

Let:
- \( p \) = opponent’s estimated win probability
- \( P \) = pot size

Then the **minimum bet** to discourage a call is:
$$
B > \frac{p}{1 - p} \cdot P
$$

---

## Quick Calculation

> 21624 / 750

$$
\frac{21624}{750} = 28.832
$$

---

Let me know if you'd like a Python function or chart for estimating bets at the table!
