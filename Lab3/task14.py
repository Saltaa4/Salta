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
