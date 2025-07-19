from itertools import product

if __package__:
    from .cards import *
else:
    from cards import *

class Deck(list):
    def __init__(self):
        super().__init__()
        for c in product(RANKS, ASCII_SUITS):
            self.append(Card(c))

if __name__ == "__main__":
    print(Deck())