import sys
import unittest

sys.path.append("..")
sys.path.append("../../src")

from calciumlang.error import OutOfRangeError

from run_test import run_calcium


class TestOutOfRange(unittest.TestCase):
    def test_out_of_range(self):
        with self.assertRaises(OutOfRangeError):
            run_calcium("out_of_range.py")


unittest.main()
