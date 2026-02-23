# Deep Diff

import json

def j(x):
    return json.dumps(x, separators=(',', ':'))

def diff(a, b, path=""):
    res = []
    keys = set(a.keys()) | set(b.keys())

    for k in keys:
        p = f"{path}.{k}" if path else k

        if k not in a:
            res.append(f"{p} : <missing> -> {j(b[k])}")
        elif k not in b:
            res.append(f"{p} : {j(a[k])} -> <missing>")
        elif isinstance(a[k], dict) and isinstance(b[k], dict):
            res += diff(a[k], b[k], p)
        elif a[k] != b[k]:
            res.append(f"{p} : {j(a[k])} -> {j(b[k])}")

    return res

A = json.loads(input())
B = json.loads(input())

ans = sorted(diff(A, B))
if ans:
    for line in ans:
        print(line)
else:
    print("No differences")