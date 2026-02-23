# Query Engine

import json
import re

data = json.loads(input())
q = int(input())

for _ in range(q):
    query = input()
    cur = data
    try:
        parts = re.split(r'\.(?![^\[]*\])', query)
        for part in parts:
            while '[' in part:
                name, rest = part.split('[', 1)
                if name:
                    cur = cur[name]
                idx, rest = rest.split(']', 1)
                cur = cur[int(idx)]
                part = rest
            if part:
                cur = cur[part]
        print(json.dumps(cur, separators=(',', ':')))
    except:
        print("NOT_FOUND")