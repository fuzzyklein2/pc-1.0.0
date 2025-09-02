""" poker_games.py

    Refactors the Driver and PokerTable into a single class.
"""
from cmd import Cmd
from io import StringIO
import sys

from eval7 import evaluate, handtype
from holdem_calc import calculate
from rich import print as rp
from rich.table import Table

if __package__:
    from .cards import Card, RANKS, VALID_CHARS
    from .hands import Hand
    from .program import Program
    from .simulate import simulate_win_probability
    from .startup import *
    from .tables import PokerTable
else:
    from cards import RANKS, VALID_CHARS
    from hands import Hand
    from program import Program
    from simulate import simulate_win_probability
    from startup import *
    from tables import PokerTable

PROMPTS = ['hand', 'flop', 'turn', 'river']

class PokerGame(list[card], Cmd, Program):

    def __init__(self):
        log.info("Initializing the `PokerGame` object...")
        list.__init__()
        Cmd.__init__(self)
        Program.__init__(self)
        self.max_num_players = n if n <= 10 else print("ERROR: Invalid input!")
        self.cur_num_players = i if i <= n else print("ERROR: Invalid input!")
        self.num_still_in = self.cur_num_players
        self.disconnected = 0
        # self.status = 0
