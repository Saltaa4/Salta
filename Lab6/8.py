# Sorted Unique Numbers (set + sorted)

n = int(input())
nums = list(map(int, input().split()))

unique = sorted(set(nums))
print(*unique)