"""
    cards.py

    The card object should be initialized by a 2 char string.
    One character for the index 0..12 and another for the
    suit [cdhs]. Each will have its own output string,
    which may contain unicode points for the suits.

    Data variables should include:

        * index
        * suit

    The __str__ and __repr__ functions should be overrideen.
    
"""
import eval7
from rich import print as rprint

if __package__:
    from .integers import Integer
else:
    from integers import Integer

ACE = 'A'
KING = 'K'
QUEEN = 'Q'
JACK = 'J'
TEN = 'T'
SUITS = '♣♦♥♠'
ASCII_SUITS = 'cdhs'
RANKS = '23456789TJQKA'
VALID_CHARS = RANKS + ASCII_SUITS + 'tjqka'
FOLD_CHARS = 'fF'
VALID_RANK_CHARS = RANKS + 'tjqka'
VALID_SUIT_CHARS = ASCII_SUITS + ASCII_SUITS.lower()

PICTS = dict(zip(list(ASCII_SUITS), list(SUITS)))
# for i in range(4):
    # PICTS[ASCII_SUITS[i]] = SUITS[i]
    
BAD_INPUT_STR = "[red]ERROR[/]: Bad input!"

class InputError(Exception):
    pass
    
class Card(eval7.Card):
    def __init__(self, /, *args, **kwargs):
        if type(args[0]) is Card:
            args = (str(args[0]))
        eval7.Card.__init__(*args, **kwargs)

        self._ascii_rank = RANKS[self.rank]
        self._ascii_suit = ASCII_SUITS[self.suit]
        self._pict = SUITS[self.suit]

    def __str__(self):
        return self._ascii_rank + self.pict

    @property
    def ascii_rank(self):
        return self._ascii_rank
        
    @ascii_rank.setter
    def ascii_rank(self, value):
        self.ascii_rank = value
        
    @property
    def ascii_suit(self):
        return self._ascii_suit
        
    @ascii_suit.setter
    def ascii_suit(self, value):
        self._ascii_suit = value

    def output(self):
        return self.ascii_rank + self.pict

    @property
    def pict(self):
        return self._pict

    @pict.setter
    def pict(self, c):
        self._pict = c

    @staticmethod
    def is_valid_card_string(s):
        num_folds = 0
        logical_index = Integer(0)
        current_rank = None
        cards = list()
        s = ''.join(s.split())
        # print(s)
        for c in s:
            # print(c)
            if c in FOLD_CHARS:
                num_folds += 1
            elif logical_index.is_even():
                if c in VALID_RANK_CHARS:
                    current_rank = c.upper()
                    logical_index += 1
                else:
                    rprint(BAD_INPUT_STR)
            elif logical_index.is_odd():
                if c in VALID_SUIT_CHARS:
                    cards.append(Card(current_rank + c.lower()))
                    current_rank = None
                    logical_index += 1
                else:
                    rprint(BAD_INPUT_STR)
        return (cards, num_folds)