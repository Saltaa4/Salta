import re

s = input()

def double(m):
    return m.group() * 2

print(re.sub(r"\d", double, s))