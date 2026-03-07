import re

s = input()

pattern = re.compile(r"\b\w+\b")

print(len(pattern.findall(s)))