def isUsual(num: int) -> bool:
    
    while num % 2 == 0:
        num //= 2
    while num % 3 == 0:
        num //= 3
    while num % 5 == 0:
        num //= 5
    
    return num == 1

n = int(input())

if isUsual(n):
    print("Yes")
else:
    print("No")


# Разделяем число на множители 2, 3 и 5
# Если после всех делений число стало 1, значит оно состоит только из множителей 2, 3 и 5: return num == 1
# Чтение входных данных
# Выводим результат в зависимости от возвращаемого значения функции
