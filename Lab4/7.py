# Reverse Iterator

class Reverse:
    def __init__(self, s):
        self.s = s
        self.i = len(s) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < 0:
            raise StopIteration
        ch = self.s[self.i]
        self.i -= 1
        return ch

s = input()
for ch in Reverse(s):
    print(ch, end="")