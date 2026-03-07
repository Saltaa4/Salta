line = list(map(int, input().split()))

avg =  sum(line) / len(line)
count = 0

for x in line:
    if x > avg:
        count += 1

print(count)






"""
In this task, you should count how many numbers are strictly greater than the average value of the list.

Input format
A line of integers separated by spaces.

Output format
Output the count.

Examples

Input
1 2 3 4

Output
2
# Print how many numbers are strictly greater than the average of the list.

"""




