a = int(input())
b = int(input())

count = 0

for i in range(a, b + 1):
    if i % 2 == 0:
        count += 1

print(count)




"""
B: Even in Range
In this task, you should count how many even numbers are in the interval [a, b].

Input format
Two integers a and b (−10^6 ≤ a ≤ b ≤ 10^6)

Output format
Output the count.

Examples

Input
3
9

Output
3
"""