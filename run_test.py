import unittest
from contextlib import redirect_stdout
import io
import os

from calciumlang import Runtime
from converter import convert
import sys
import json

dir_name = sys.argv[1]


def run_calcium(filepath):
    with open(filepath) as fin:
        text = fin.read()
        json_text = convert(text)
        code = json.loads(json_text)
        runtime = Runtime(code)
        runtime.run()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    for filename in os.listdir(dir_name):
        if not filename.endswith(".py"):
            continue
        testname = filename[:-3]
        filepath = os.path.join(os.getcwd(), dir_name, filename)

        def make_test(filepath):
            def test_file(self):
                with io.StringIO() as raw_out, io.StringIO() as calcium_out:
                    with redirect_stdout(raw_out):
                        with open(filepath) as fin:
                            exec(fin.read(), {})
                    with redirect_stdout(calcium_out):
                        run_calcium(filepath)
                    self.assertEqual(raw_out.getvalue(), calcium_out.getvalue())

            return test_file

        methodname = "test_{}".format(filename)
        testcase = type(
            testname, (unittest.TestCase,), {methodname: make_test(filepath)}
        )
        suite.addTest(testcase(methodName=methodname))
    unittest.TextTestRunner().run(suite)
