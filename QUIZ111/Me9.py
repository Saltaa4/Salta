n = int(input())
pairs = []

for _ in range(n):
    a, b = map(int, input().split())
    pairs.append((a, b))

pairs.sort(key=lambda x: x[1])

for pair in pairs:
    print(pair[0], pair[1])







"""
I: Lambda Sort
In this task, you are given pairs of numbers.
Sort them by the second element using a lambda function.

Input format
n — number of pairs
Then n lines: two integers per line.

Output format
Print pairs sorted by the second element.

Example

Input
3
1 5
2 3
4 1

Output
4 1
2 3
1 5
"""