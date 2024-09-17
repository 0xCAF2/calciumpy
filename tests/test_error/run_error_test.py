import sys
import unittest

sys.path.append("..")
sys.path.append("../../src")

from calciumlang.error import OutOfRangeError, NameNotFoundError, ObjectNotIterableError

from run_test import run_calcium


class TestOutOfRange(unittest.TestCase):
    def test_out_of_range(self):
        with self.assertRaises(OutOfRangeError):
            run_calcium("out_of_range.py")

    def test_name_not_found(self):
        with self.assertRaises(NameNotFoundError):
            run_calcium("name_not_found.py")

    def test_object_not_iterable(self):
        with self.assertRaises(ObjectNotIterableError):
            run_calcium("object_not_iterable.py")


unittest.main()
