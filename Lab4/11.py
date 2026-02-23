# JSON Patch Update

import json

def patch(src, p):
    for key in p:
        if p[key] is None:
            src.pop(key, None)
        elif key in src and isinstance(src[key], dict) and isinstance(p[key], dict):
            patch(src[key], p[key])
        else:
            src[key] = p[key]
    return src

source = json.loads(input())
patch_obj = json.loads(input())

result = patch(source, patch_obj)
print(json.dumps(result, separators=(',', ':'), sort_keys=True))