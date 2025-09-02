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
from rich import print as rp
from rich.table import Table

if __package__:
    from .cards import Card
    from .hands import *
    from .simulate import simulate_win_probability
    from .startup import *
else:
    from cards import Card
    from hands import *
    from simulate import simulate_win_probability
    from startup import *
    
class PokerTable(list[Card]):
    def __init__(self, n, i):
        log.info("Setting up the poker table...")
        super().__init__()
        self.max_num_players = n if n <= 10 else print("ERROR: Invalid input!")
        self.cur_num_players = i if i <= n else print("ERROR: Invalid input!")
        self.num_still_in = self.cur_num_players
        self.disconnected = 0
        # self.status = 0
                
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
        rp(f"Removed {n} players.")
        rp(f"{self.cur_num_players} players remaining.")

    def add(self, n):
        self._cur_num_players += n
        rp(f"Added {n} players.")
        rp(f"{self.cur_num_players} players now present.")

    def fold(self, n):
        self._num_still_in -= n
        rp(f"Folded {n} players.")
        rp(f"{self.num_still_in} players are still in.")

    def reset(self):
        self.clear()
        self._num_still_in = self._cur_num_players
        # self.fold(self.disconnected)
        rp(f"PokerTable reset. {self.num_still_in} players.")
        rp(f"{self.disconnected} players disconnected.")
    
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
            return Turn([self[5]])
        else: return None

    @property
    def river(self):
        if len(self) == 7:
            return River([self[6]])
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
            
    # @status.setter
    # def status(self, i):
        # self._status = i

    def __iadd__(self, s: str):
        v = Card.is_valid_card_string(s)
        if v:
            if len(v[0]) == 2 and len(self):
                self.reset()
            self.extend(v[0])
            if len(self) == 5:
                rp(f"Flop: {self.flop}")
            elif len(self) == 6:
                rp(f"Turn: {self.turn}")
            elif len(self) == 7:
                rp(f"River: {self.river}")
            if v[1]:
                self.fold(v[1])
            self.revise()
            # rp(f"Current status: {self.status}")
        else:
            print("ERROR: Bad input.")
        return self

    def revise(self):
        # print("Revising hand equity...")
        match len(self):
            case 2:
                # print(f"{self.hand.equity(self.num_still_in)=}")
                equity = self.hand.equity(self.num_still_in - self.disconnected)
                if equity:
                    rp(f"Hand: {self.hand.output()}\nEquity: {round(equity*100, 2)}%")
            case 5 | 6 | 7:
                # print("Flop, Turn, River...")
                print()
                # Really should check for faulty input here.
                # print(self)
                print(handtype(evaluate(self)))
                print()
                # breakpoint()
                oldout = sys.stdout
                s = StringIO()
                sys.stdout = s
                # if VERBOSE: help(calculate)
                calculate(list(map(lambda c: c.ascii_rank + c.ascii_suit, self[2:])),
                          True, 500, None,
                          list(map(lambda c: c.ascii_rank + c.ascii_suit, self[0:2])),
                          True)
                sys.stdout = oldout
                # print()
                # print("Output from holdem_calc...")
                # print(s.getvalue())
                # print()
                
                lines = s.getvalue().split('\n')[5:-3]
                
                t = Table("Hand", "Probability", "Odds")
                
                for l in lines:
                    words = l.split(':')
                    hand = words[0].strip()
                    prob = round(float(words[1].strip()), 2) * 100
                    odds = ((100 - prob) / prob) if prob else '∞'
                    if prob > 0:
                        t.add_row(hand, f"{prob}%", f"{round(odds, 1)} : 1")
                
                rp(t)
                
                # print('\n'.join(lines))
                print()
                simulate_win_probability(list(map(lambda c: c.ascii_rank + c.ascii_suit, self.hand)),
                                         list(map(lambda c: c.ascii_rank + c.ascii_suit, self[2:])),
                                         self.num_still_in - self.disconnected,
                                         num_simulations=5000)
                # print()

    @property
    def disconnected(self):
        return self._disconnected
        
    @disconnected.setter
    def disconnected(self, n):
        self._disconnected = n
        
    def disconnect(self, n):
        self.disconnected += n
        rp(f"Disconnected {n} player{'s' if n > 1 else ''}.")
        rp(f"{self.cur_num_players} are at the table.")
        rp(f"{self.disconnected} are disconnected.")
        
    def connect(self, n):
        self.disconnected -= n
        rp(f"Connected {n} player{'s' if n > 1 else ''}.")
        rp(f"{self.cur_num_players} are at the table.")
        rp(f"{self.disconnected} are disconnected.")

    @property
    def num_active_players(self):
        return self.cur_num_players - self.disconnected

    