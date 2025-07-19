import eval7
import pandas as pd

if __package__:
    from .cards import Card
else:
    from cards import Card

PROBABILITIES = pd.read_pickle('data/probabilities.pkl')

class Hand(list[Card]):
    def __init__(self, cards=None):
        print(f"Initializing Hand object. {cards=}")
        if cards:
            # self.extend(list(map(Card, cards)))
            for c in cards:
                if type(c) is Card:
                    self.append(c)
                else:
                    self.append(Card(c))
        
    def output(self):
        return ' '.join([c.output() for c in self]) if self else None

    @property
    def max_size(self):
        return 2

    @property
    def key(self):
        suited = 's' if self[0].suit == self[1].suit else ''
        s = self[0].ascii_rank + self[1].ascii_rank + suited
        print("Making a key for the hand...")
        print("First try:", s)
        if not s in PROBABILITIES.index:
            s = self[1].ascii_rank + self[0].ascii_rank + suited
            print("Second try:", s)
            if not s in PROBABILITIES.index:
                return None
        return s

    def equity(self, n):
        p = None
        try:
            print(f"{self.key=}")
            p = PROBABILITIES.at[(self.key, str(n))] / 100
        except KeyError:                        
            print("Bad input. Table key not found!")
        return p