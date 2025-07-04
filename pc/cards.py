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
ACE = 'A'
KING = 'K'
QUEEN = 'Q'
JACK = 'J'
TEN = 'T'
SUITS = '♣♦♥♠'
ASCII_SUITS = 'cdhs'
RANKS = '23456789TJQKA'
VALID_CHARS = RANKS + ASCII_SUITS + 'tjqka'

PICTS = dict()
for i in range(3):
    PICTS[ASCII_SUITS[i]] = SUITS[i]

class Card(eval7.Card):
    def __init__(self, /, *args, **kwargs):
        """ c must be a string with 2 chars.
            The first must be an uppercase letter if it is a letter.
            The 2nd must be lowercase, representing the suit of the card.
        """
        args = (args[0][0].upper() + args[0][1].lower())
        eval7.Card.__init__(*args, **kwargs)

        self._ascii_rank = RANKS[self.rank]
        self._ascii_suit = ASCII_SUITS[self.suit]
        self._pict = SUITS[self.suit]

    def __str__(self):
        return self._ascii_rank + self._pict

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
        return self.rank + self.pict