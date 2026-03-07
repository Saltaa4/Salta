def max_difference(lst):
    return max(lst) - min(lst)

nums = list(map(int, input().split()))
print(max_difference(nums))



"""
H: Function Max Difference
In this task, create a function that returns the difference between the maximum and minimum of a list.

Input format
A line of integers.

Output format
Print the result.

Example

Input
4 1 9 3

Output
8
"""