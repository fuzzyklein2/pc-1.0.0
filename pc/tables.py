"""
    tables.py

    Despite the name, a table here is just a list of cards.
    It may contain 5 of them at the most.
    It also has a certain number of players sitting at it.
"""
class PokerTable(object):
    def __init__(self, n, i):
        super().__init__()
        self._max_num_players = n if n <= 10 else print("ERROR: Invalid input!")
        self._cur_num_players = i if i <= n else print("ERROR: Invalid input!")
        self._num_still_in = self.cur_num_players
        
    @property
    def max_num_players():
        return self._max_num_players
        
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
        self._num_still_in = self._cur_num_players
    

