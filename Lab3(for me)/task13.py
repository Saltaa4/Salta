def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

nums = [int(x) for x in input().split()]

primes = list(filter(lambda x: is_prime(x), nums))

if len(primes) > 0:
    print(*(primes))
else:
    print("No primes")













# Создаем обычную функцию для проверки, является ли число простым (L3.1).
def is_prime(n):
    # Числа меньше 2 (0, 1) не являются простыми.
    if n < 2:
        return False
    # Проверяем делители от 2 до корня из n (L2.2).
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            # Если число на что-то делится без остатка, оно не простое.
            return False
    return True

# Считываем ввод, разбиваем его и превращаем каждый элемент в число (L1.7, L2.3).
# Мы используем цикл внутри списка (List Comprehension), чтобы быстро получить список int.
nums = [int(x) for x in input().split()]

# Используем filter() и lambda (L3.3).
# Lambda x: is_prime(x) — это короткая анонимная функция.
# Она берет каждое число x из списка и "пропускает" его через is_prime.
# filter() оставляет только те элементы, для которых результат True.
primes_iter = filter(lambda x: is_prime(x), nums)

# Превращаем результат фильтрации обратно в обычный список (L2.3).
primes = list(primes_iter)

# Проверяем, нашлись ли простые числа (L1.10 Booleans, L1.12 Conditions).
if len(primes) > 0:
    # Выводим список через пробел. Символ * "распаковывает" список для print.
    print(*(primes))
else:
    # Если список пуст, выводим сообщение по условию.
    print("No primes")