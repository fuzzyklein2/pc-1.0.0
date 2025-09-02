from cmd import Cmd
from io import StringIO
import sys

from holdem_calc import calculate
import pandas as pd

from eval7 import evaluate, handtype

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

class Driver(Cmd, Program):
    def __init__(self):
        log.info("Initializing the `Cmd` object...")
        Cmd.__init__(self)
        Program.__init__(self)
        self.status = 0
   
    def run(self):
        super().cmdloop()

    def do_quit(self, args):
        return True

    def do_ask(self, args):
        pass

    def preloop(self):
        """Called once when the cmdloop() method is called, before entering the command loop."""
        print(f"Welcome to {PROGRAM}!")
        print("Type 'help' for a list of commands.")
        self.poker_table = PokerTable(int(input("Enter the maximum number of players at the table: ")),
                                      int(input("Enter the number of players currently at the table: ")))
        if VERBOSE:
            print("PokerTable object initialized.")
        # self.hand = Hand()
        print()
        self.prompt = f"Ready for {'the' if self.poker_table.status else 'a'} {PROMPTS[self.poker_table.status]}: "

    def do_done(self, line):
        self.poker_table.reset()
        print()
        self.prompt = f"Ready for {'the' if self.poker_table.status else 'a'} {PROMPTS[self.poker_table.status]}: "

    # def revise(self):
        # self.poker_table.revise()
        
    def default(self, line):
        """Called when the input command does not match any do_ methods."""
        self.poker_table += line
        if self.poker_table.status >= 4:
            self.prompt = "Ready for input: "
        else:
            self.prompt = f"Ready for {'the' if self.poker_table.status else 'a'} {PROMPTS[self.poker_table.status]}: "
                    
    # def rank2key(self, n):
        # return RANKS.find(str(n))

    def do_remove(self, line):
        n = 1
        if line:
            n = int(line)
        self.poker_table.remove(n)
        print(f"Players currently at the table: {self.poker_table.cur_num_players}")
        self.poker_table.revise()
        print()

    def do_add(self, line):
        n = 1
        if line:
            n = int(line)
        self.poker_table.add(n)
        print(f"Players currently at the table: {self.poker_table.cur_num_players}")
        self.poker_table.revise()
        print()

    def do_fold(self, line):
        self.poker_table.fold(int(line))
    
    def do_disc(self, line):
        self.poker_table.disconnect(int(line))
        
    def do_conn(self, line):
        self.poker_table.connect(int(line))