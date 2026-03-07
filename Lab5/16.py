import re

s = input()

m = re.search(r"Name:\s*(.+),\s*Age:\s*(\d+)", s)
print(m.group(1), m.group(2))