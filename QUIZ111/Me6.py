nums = list(map(int, input().split()))
freq = {}

for num in nums:
    freq[num] = freq.get(num, 0) + 1

for key in sorted(freq):
    print(key, freq[key])





"""
F: Dictionary Frequency
In this task, you should count how many times each number appears.

Input format
A line of integers.

Output format
For each distinct number (in ascending order), print:
number count

Examples

Input
1 2 2 3

Output
1 1
2 2
3 1
"""