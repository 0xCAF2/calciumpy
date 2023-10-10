import sys

sys.path.append("../src")
sys.path.append("../tools")

from calciumlang.runtime import Runtime, RuntimeResult

from converter import convert

import json

s = """
t = input('test:')
print(t)
print(input(len(input(input(t)))))
"""
code = convert(s)
# print(code)
r = Runtime(json.loads(code))
result = r.run()
while True:
    if result == RuntimeResult.PAUSED:
        t = input(r.env.prompt)
        result = r.resume(t)
        continue
    elif result == RuntimeResult.EXECUTED:
        result = r.run()
    else:
        break
