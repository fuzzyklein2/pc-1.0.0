from cmd import Cmd
# import tkinter as tk
# from tkinter import messagebox

if __package__:
    from .startup import *
else:
    from startup import *


import pandas as pd

from .program import Program
from .startup import PROGRAM
import sys

class Driver(Cmd, Program):
    def run(self):
        # self.process_files()
        super().cmdloop()

    def do_quit(self, args):
        pass    
    #     root = tk.Tk()
    #     root.withdraw()  # Hide the main window
        
    #     # Show the dialog
    #     response = messagebox.askyesnocancel("Question", f"Do you really want to quit {PROGRAM}?")
        
    #     # Destroy the root window after the dialog is closed
    #     root.destroy()
        
    #     # Handle responses
        return True

    def do_ask(self, args):
        pass

    def preloop(self):
        """Called once when the cmdloop() method is called, before entering the command loop."""
        self.PROBABILITIES = pd.read_csv('data/probabilities.csv')
        if VERBOSE:
            print("Probability table loaded.")
            print(self.PROBABILITIES)
        # Need to know the maximum number of players at the table.
        try:
            self.max_players = int(input("Enter the maximum number of players at the table: "))
        except ValueError:
            print("Invalid input. Using default value.")
            self.max_players = 8  # or any sensible default
        try:
            self.cur_num_players = int(input("Enter the current number of players at the table: "))
        except ValueError:
            print("Invalid input. Using default value.")
            self.cur_num_players = 2
        print(f"Maximum number of players set to {self.max_players}.")
        print(f"Welcome to {PROGRAM}!")
        print("Type 'help' for a list of commands.")
        self.players_still_in = self.cur_num_players

    def default(self, line):
        """Called when the input command does not match any do_ methods."""
        print("Ready for the next hand.")
        # print(line)
        
        return None
    