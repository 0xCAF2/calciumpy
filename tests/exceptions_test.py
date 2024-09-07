import unittest

import json
import sys

sys.path.append("../src")

from calciumlang.runtime import Runtime
from calciumlang.tools.converter import convert

testfilename = sys.argv[1]


def run_calcium(filepath):
    with open(filepath) as fin:
        text = fin.read()
        json_text = convert(text)
        code = json.loads(json_text)
        runtime = Runtime(code)
        runtime.run()


if __name__ == "__main__":
    unittest.TextTestRunner().run(
        unittest.FunctionTestCase(lambda: run_calcium(testfilename))
    )
