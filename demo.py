from src.calciumlang.tools.converter import convert
import json
from src.calciumlang.runtime import Runtime

# "converter" can read the subset of Python code and
# generates Calcium code.
calcium_code = convert(
    """
# write Python source code here
message = 'Hello, World.'
print(message)
"""
)

# A Runtime executes Calcium code which is given as JSON array.
runtime = Runtime(calcium_code)
runtime.run()  # outputs 'Hello, World.'
