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
        Cmd.__init__(self)
        Program.__init__(self)
        self.status = 0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value > len(PROMPTS):
            self._status = int(input("Invalid status! Please enter the actual status: "))
        else:
            self._status = value
    
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
        if VERBOSE:
            print("Probability table loaded.")
            print(self.PROBABILITIES)
        self.poker_table = PokerTable(int(input("Enter the maximum number of players at the table: ")),
                                      int(input("Enter the number of players currently at the table: ")))
        if VERBOSE:
            print("PokerTable object initialized.")
        self.hand = Hand()
        print()
        self.prompt = f"Ready for the {PROMPTS[self.status]}: "

    def do_done(self, line):
        self.hand = Hand()
        self.status = 0
        self.poker_table.reset()
        print()
        self.prompt = f"Ready for the {PROMPTS[self.status]}: "

    def revise(self):
        match(len(self.hand)):
            case 2:
                suited = self.hand[0].suit == self.hand[1].suit
                # DEBUG: String indices must be int, not str...
                key = f"{RANKS[self.hand[0].rank]}{RANKS[self.hand[1].rank]}{'s' if suited else ''}"
                try:
                    p = self.PROBABILITIES.at[(key, str(self.poker_table.num_still_in))] / 100
                except KeyError:                        
                    key = f"{RANKS[self.hand[1].rank]}{RANKS[self.hand[0].rank]}{'s' if suited else ''}"
                    try:
                        p = self.PROBABILITIES.at[(key, str(self.poker_table.num_still_in))] / 100
                    except KeyError:
                        print("Bad input. Table key not found!")
                        return False
                print(f"Revised win probability: {p}")
            case 5 | 6 | 7:
                print(handtype(evaluate(self.hand)))
                oldout = sys.stdout
                s = StringIO()
                sys.stdout = s
                calculate(list(map(str, self.hand[2:])),
                          True, 500, None,
                          list(map(str, self.hand[0:2])),
                          True)
                sys.stdout = oldout
                print('\n'.join(s.getvalue().split('\n')[5:-3]))
                print()
                simulate_win_probability(list(map(str, self.hand[0:2])),
                                         list(map(str, self.hand[2:-1])),
                                         self.poker_table.num_still_in)
                print()

        
    def default(self, line):
        """Called when the input command does not match any do_ methods."""
        if not (line[0] in VALID_CHARS or line[0] == 'f'):
            print("Invalid input. Try again.")
            return False
        if line.startswith('f'):
            n = line.count('f')
            self.poker_table.fold(n)
            print(f"{n} folded. {self.poker_table.num_still_in} still in.")
            self.revise()
            return False
        else:
            cards = [f"{c[0].upper()}{c[1].lower()}" for c in line.split()]
            # print(cards)
            for c in cards:
                self.hand.append(Card(c))
            # print(self.hand)
            match(len(self.hand)):
                case 2:
                    suited = self.hand[0].suit == self.hand[1].suit
                    if VERBOSE:
                        print(self.hand)
                        print(self.hand[0])
                        print(self.hand[1])
                    key = f"{RANKS[self.hand[0].__str__()[0]]}{RANKS[self.hand[1].rank]}{'s' if suited else ''}"
                    try:
                        p = self.PROBABILITIES.at[(key, str(self.poker_table.num_still_in))] / 100
                    except KeyError:                        
                        key = f"{RANKS[self.hand[1].rank]}{RANKS[self.hand[0].rank]}{'s' if suited else ''}"
                        try:
                            p = self.PROBABILITIES.at[(key, str(self.poker_table.num_still_in))] / 100
                        except KeyError:
                            print("Bad input. Table key not found!")
                            return False
                    # Print the pre-flop probability of the hand winning.
                    print(f"Pre-Flop Probability for {self.hand.output()}: {p * 100}%")
                    # print()
                case 5 | 6 | 7:
                    print()
                    # Really should check for faulty input here.
                    print(handtype(evaluate(self.hand)))
                    print()
                    oldout = sys.stdout
                    s = StringIO()
                    sys.stdout = s
                    calculate(list(map(str, self.hand[2:])),
                              True, 500, None,
                              list(map(str, self.hand[0:2])),
                              True)
                    sys.stdout = oldout
                    print('\n'.join(s.getvalue().split('\n')[5:-3]))
                    print()
                    simulate_win_probability(list(map(str, self.hand[0:2])),
                                             list(map(str, self.hand[2:-1])),
                                             self.poker_table.num_still_in,
                                             num_simulations=10000)
                    # print()
        if len(self.hand) < 7:
            self.status += 1
        else:
            return self.do_done(line)
        print()
        self.prompt = f"Ready for the {PROMPTS[self.status]}: "

                    
    def rank2key(self, n):
        return RANKS.find(str(n))

    def do_remove(self, line):
        n = 1
        if line:
            n = int(line)
        self.poker_table.remove(n)
        print(f"Players currently at the table: {self.poker_table.cur_num_players}")
        self.revise()
        print()

    def do_add(self, line):
        n = 1
        if line:
            n = int(line)
        self.poker_table.add(n)
        print(f"Players currently at the table: {self.poker_table.cur_num_players}")
        self.revise()
        print()

    