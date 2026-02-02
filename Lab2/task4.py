n = int(input())
numbers = list(map(int, input().split()))

count_positive = 0
for x in numbers:
  if x > 0:
    count_positive += 1
    
print(count_positive)