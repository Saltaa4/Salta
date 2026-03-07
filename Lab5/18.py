import re

s = input()
p = input()

pattern = re.escape(p)

print(len(re.findall(pattern, s)))