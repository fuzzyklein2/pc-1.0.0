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
class Card(object):
    ACE = 'A'
    KING = 'K'
    QUEEN = 'Q'
    JACK = 'J'
    TEN = 'T'
    SUITS = 'shdc'
    RANKS = '23456789TJQKA'

    def __init__(rank, suit):
        super().__init__()
        self.rank = rank.upper() if rank in RANKS else 0
        self.suit = suit.lower() if suit in SUITS else 0

    
