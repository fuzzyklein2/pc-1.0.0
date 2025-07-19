class Integer(int):
    def is_even(self):
        return self % 2 == 0

    def is_odd(self):
        return self % 2 != 0

    def is_positive(self):
        return self > 0

    def is_negative(self):
        return self < 0

    def __iadd__(self, value):
        return Integer(self + value)