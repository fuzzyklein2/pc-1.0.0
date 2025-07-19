"""
    tables.py

    Despite the name, a table here is just a list of cards.
    It may contain 5 of them at the most.
    It also has a certain number of players sitting at it.
"""
from io import StringIO
import sys

from eval7 import evaluate, handtype
from holdem_calc import calculate

if __package__:
    from .cards import Card
    from .hands import Hand
    from .simulate import simulate_win_probability
    from .startup import *
else:
    from cards import Card
    from hands import Hand
    from simulate import simulate_win_probability
    from startup import *
    
class PokerTable(list[Card]):
    def __init__(self, n, i):
        log.info("Setting up the poker table...")
        super().__init__()
        self.max_num_players = n if n <= 10 else print("ERROR: Invalid input!")
        self.cur_num_players = i if i <= n else print("ERROR: Invalid input!")
        self.num_still_in = self.cur_num_players
        self.status = 0
                
    @property
    def max_num_players():
        return self._max_num_players

    @max_num_players.setter
    def max_num_players(self, n):
        self._max_num_players = n
        
    @property
    def cur_num_players(self):
        return self._cur_num_players

    @cur_num_players.setter
    def cur_num_players(self, value):
        self._cur_num_players = value

    @property
    def num_still_in(self):
        return self._num_still_in

    @num_still_in.setter
    def num_still_in(self, value):
        self._num_still_in = value

    def remove(self, n):
        self._cur_num_players -= n

    def add(self, n):
        self._cur_num_players += n

    def fold(self, n):
        self._num_still_in -= n

    def reset(self):
        list.__init__()
        self._num_still_in = self._cur_num_players
        self.status = 0
    
    @property
    def hand(self):
        if self[0] and self[1]:
            return Hand(self[0:2])
        else:
            return None

    @property
    def flop(self):
        if len(self) >= 5:
            return Flop(self[2:5])
        else: return None

    @property
    def turn(self):
        if len(self) >= 6:
            return Turn(self[5])
        else: return None

    @property
    def river(self):
        if len(self) == 7:
            return River(self[6])
        else: return None

    @property
    def status(self):
        match len(self):
            case 0:
                return 0
            case 2:
                return 1
            case 5:
                return 2
            case 6:
                return 3
            case 7:
                return 4
            
    @status.setter
    def status(self, i):
        self._status = i

    def __iadd__(self, s: str):
        v = Card.is_valid_card_string(s)
        if v:
            self.extend(v[0])
            self.fold(v[1])
            self.revise()
            self.status += 1
        else:
            print("ERROR: Bad input.")
        return self

    def revise(self):
        print("Revising hand equity...")
        match len(self):
            case 2:
                print(f"{self.hand.equity(self.num_still_in)=}")
            case 5 | 6 | 7:
                # print("Flop, Turn, River...")
                print()
                # Really should check for faulty input here.
                print(self)
                print(handtype(evaluate(self)))
                print()
                oldout = sys.stdout
                s = StringIO()
                sys.stdout = s
                if VERBOSE: help(calculate)
                calculate(list(map(str, self[2:])),
                          True, 500, None,
                          list(map(str, self[0:2])),
                          True)
                sys.stdout = oldout
                print()
                print("Output from holdem_calc...")
                print(s.getvalue())
                print()
                print('\n'.join(s.getvalue().split('\n')[5:-3]))
                print()
                simulate_win_probability(list(map(str, self.hand)),
                                         list(map(str, self[2:])),
                                         self.num_still_in,
                                         num_simulations=5000)
                # print()
