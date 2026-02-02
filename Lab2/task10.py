n = int(input())
numbers = list(map(int, input().split()))

numbers.sort()
numbers.reverse()

for x in numbers:
    print(x, end=" ")



# сортирует список по возрастанию
# переворачивает список
