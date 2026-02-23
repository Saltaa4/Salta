# Shortest Path Around Circle

import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

def dist(xa, ya, xb, yb):
    return math.hypot(xb - xa, yb - ya)

def segment_hits_circle(ax, ay, bx, by, r):
    dx, dy = bx - ax, by - ay
    A = dx * dx + dy * dy
    B = 2 * (ax * dx + ay * dy)
    C = ax * ax + ay * ay - r * r
    if A == 0:
        return ax * ax + ay * ay < r * r
    D = B * B - 4 * A * C
    if D <= 0:
        return False
    s = math.sqrt(D)
    t1 = (-B - s) / (2 * A)
    t2 = (-B + s) / (2 * A)
    lo, hi = sorted([t1, t2])
    return hi > 0 and lo < 1

direct = dist(x1, y1, x2, y2)

if not segment_hits_circle(x1, y1, x2, y2, R):
    print(f"{direct:.10f}")
else:
    ra = math.hypot(x1, y1)
    rb = math.hypot(x2, y2)

    dot = x1 * x2 + y1 * y2
    cos_theta = dot / (ra * rb)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    theta = math.acos(cos_theta)

    alpha = math.acos(R / ra)
    beta = math.acos(R / rb)

    arc = theta - alpha - beta
    if arc < 0:
        arc = 0.0

    ta = math.sqrt(ra * ra - R * R)
    tb = math.sqrt(rb * rb - R * R)

    ans = ta + tb + R * arc
    print(f"{ans:.10f}")