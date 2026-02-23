# Radar Coverage (length of segment inside circle)

import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

A = dx * dx + dy * dy
B = 2 * (x1 * dx + y1 * dy)
C = x1 * x1 + y1 * y1 - R * R

ts = [0.0, 1.0]

if A != 0:
    D = B * B - 4 * A * C
    if D >= 0:
        s = math.sqrt(D)
        t1 = (-B - s) / (2 * A)
        t2 = (-B + s) / (2 * A)
        if 0.0 <= t1 <= 1.0:
            ts.append(t1)
        if 0.0 <= t2 <= 1.0:
            ts.append(t2)

ts.sort()

seg_len = math.hypot(dx, dy)
ans = 0.0

for i in range(len(ts) - 1):
    l = ts[i]
    r = ts[i + 1]
    mid = (l + r) / 2
    xm = x1 + dx * mid
    ym = y1 + dy * mid
    if xm * xm + ym * ym <= R * R + 1e-12:
        ans += seg_len * (r - l)

print(f"{ans:.10f}")