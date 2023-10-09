from calciumlang import Runtime, RESULT_PAUSED, RESULT_EXECUTED
from tools.converter import convert

import json

s = """
t = input('test:')
print(t)
print(input(len(input(input(t)))))
"""

r = Runtime(json.loads(convert(s)))
result = r.run()
while True:
    if result == RESULT_PAUSED:
        t = input(r.env.prompt)
        result = r.resume(t)
        continue
    elif result == RESULT_EXECUTED:
        result = r.run()
    else:
        break
