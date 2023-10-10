from tools.converter import convert
import json
from src.calciumlang.runtime import Runtime

# "converter" can read the subset of Python code and
# generates Calcium code.
json_code = convert(
    """
# write Python source code here
message = 'Hello, World.'
print(message)
"""
)

calcium_code = json.loads(json_code)

# A Runtime executes Calcium code given as JSON array.
runtime = Runtime(calcium_code)
runtime.run()  # outputs 'Hello, World.'
