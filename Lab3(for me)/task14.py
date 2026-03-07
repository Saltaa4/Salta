n = int(input())
a = [int(x) for x in input().split()]
q = int(input())

for _ in range(q):
    command = input().split()
    op = command[0]
    
    if op == 'add':
        x = int(command[1])
        a = list(map(lambda val: val + x, a))
    elif op == 'multiply':
        x = int(command[1])
        a = list(map(lambda val: val * x, a))
    elif op == 'power':
        x = int(command[1])
        a = list(map(lambda val: val ** x, a))
    elif op == 'abs':
        a = list(map(lambda val: abs(val), a))

print(*(a))














# Считываем количество элементов (L1.7).
n = int(input())

# Считываем сам массив и превращаем элементы в целые числа (L2.3).
a = [int(x) for x in input().split()]

# Считываем количество операций.
q = int(input())

# Проходим циклом по количеству операций (L2.2).
for _ in range(q):
    # Каждая строка команды разбивается на части (L1.8).
    # Например, "add 5" станет ["add", "5"], а "abs" станет ["abs"].
    command = input().split()
    op = command[0] # Сама операция
    
    # Проверяем тип операции через условия (L1.12).
    if op == 'add':
        x = int(command[1])
        # map() берет lambda и применяет её к каждому элементу списка 'a'.
        # lambda val: val + x — это анонимная функция (L3.3).
        a = list(map(lambda val: val + x, a))
        
    elif op == 'multiply':
        x = int(command[1])
        # Умножаем каждый элемент на x.
        a = list(map(lambda val: val * x, a))
        
    elif op == 'power':
        x = int(command[1])
        # Возводим каждый элемент в степень x (L1.11).
        a = list(map(lambda val: val ** x, a))
        
    elif op == 'abs':
        # Применяем встроенную функцию модуля abs().
        a = list(map(lambda val: abs(val), a))

# Выводим финальный массив. 
# Символ * перед 'a' (распаковка) выведет числа через пробел без скобок (L2.3).
print(*(a))