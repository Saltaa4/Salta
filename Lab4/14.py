# Days Between (Time Zones)

from datetime import datetime, timezone, timedelta
import re

def parse(line):
    date_part, tz_part = line.split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    sign = 1 if '+' in tz_part else -1
    h, m = map(int, re.findall(r'\d+', tz_part))
    offset = timedelta(hours=h, minutes=m)
    return dt.replace(tzinfo=timezone(sign * offset))

d1 = parse(input())
d2 = parse(input())

diff = abs((d1 - d2).total_seconds())
print(int(diff // 86400))