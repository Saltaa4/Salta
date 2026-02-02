n = int(input())
numbers = list(map(int, input().split()))

max_value = numbers[0]
min_value = numbers[0]

for x in numbers:
    if x > max_value:
        max_value = x
    if x < min_value:
        min_value = x

for i in range(n):
    if numbers[i] == max_value:
        numbers[i] = min_value

for x in numbers:
    print(x, end=" ")
































# Поиск максимума и минимума: 
# берём каждый элемент x
# если он больше текущего максимума → обновляем максимум
# если он меньше текущего минимума → обновляем минимум

# Замена всех максимальных элементов на минимальные.

# x - само число из списка, i — индекс