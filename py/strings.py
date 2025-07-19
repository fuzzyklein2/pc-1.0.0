class String(str):
    def reverse(self, in_place=True):
        reversed_str = self[::-1]
        if in_place:
            return String(reversed_str)
        else:
            return reversed_str