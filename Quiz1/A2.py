s = input().strip()
count = 0

for i in range(len(s) - 1):
    if s[i] == s[i + 1]:
        count += 1

print(count)




"""
Adjacent Equal Characters
Given a string s. Count how many positions i (0 ≤ i < len(s) − 1) satisfy s[i] == s[i+1].
Print the count.

Input format
A string s.

Output format
Print one integer — the number of adjacent equal pairs.
"""