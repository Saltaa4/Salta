# Next Birthday (Time Zones)

from datetime import datetime, timezone, timedelta

def is_leap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)

def parse_date_tz(line):
    date_part, tz_part = line.split()
    y, m, d = map(int, date_part.split("-"))
    sign = 1 if "+" in tz_part else -1
    hh, mm = map(int, tz_part[4:].split(":"))
    tz = timezone(sign * timedelta(hours=hh, minutes=mm))
    return datetime(y, m, d, 0, 0, 0, tzinfo=tz)

birth = parse_date_tz(input())
now = parse_date_tz(input())

bm, bd = birth.month, birth.day
birth_tz = birth.tzinfo

now_utc = now.astimezone(timezone.utc)
year0 = now_utc.astimezone(birth_tz).year

def birthday_dt(y):
    m, d = bm, bd
    if m == 2 and d == 29 and not is_leap(y):
        d = 28
    return datetime(y, m, d, 0, 0, 0, tzinfo=birth_tz)

cand = birthday_dt(year0).astimezone(timezone.utc)
if cand < now_utc:
    cand = birthday_dt(year0 + 1).astimezone(timezone.utc)

sec = int((cand - now_utc).total_seconds())

if sec == 0:
    print(0)
else:
    print((sec + 86399) // 86400)