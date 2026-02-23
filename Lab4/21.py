# Module Query Engine

import importlib

q = int(input())
for _ in range(q):
    mod_path, attr_name = input().split()
    try:
        mod = importlib.import_module(mod_path)
    except:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(mod, attr_name):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    obj = getattr(mod, attr_name)
    print("CALLABLE" if callable(obj) else "VALUE")