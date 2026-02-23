# Log Duration (Time Zones)

from datetime import datetime, timezone, timedelta

def parse_dt(line):
    date_part, time_part, tz_part = line.split()
    y, m, d = map(int, date_part.split("-"))
    hh, mm, ss = map(int, time_part.split(":"))
    sign = 1 if "+" in tz_part else -1
    off_h, off_m = map(int, tz_part[4:].split(":"))
    tz = timezone(sign * timedelta(hours=off_h, minutes=off_m))
    return datetime(y, m, d, hh, mm, ss, tzinfo=tz)

start = parse_dt(input()).astimezone(timezone.utc)
end = parse_dt(input()).astimezone(timezone.utc)

print(int((end - start).total_seconds()))