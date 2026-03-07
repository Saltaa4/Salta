import re

s = input()

words = re.findall(r"\b[a-zA-Z]{3}\b", s)
print(len(words))