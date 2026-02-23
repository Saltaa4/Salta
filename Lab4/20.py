# Scope Accumulator

m = int(input())
g = 0
n = 0

for _ in range(m):
    scope, val = input().split()
    val = int(val)
    if scope == "global":
        g += val
    elif scope == "nonlocal":
        n += val
    # local -> ignore

print(g, n)