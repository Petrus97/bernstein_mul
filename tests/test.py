import sys
import os
sys.path.insert(0, os.path.abspath('.'))
# print(sys.path)

import unittest
from src.bernstein import add

# Test case class
class TestAddFunction(unittest.TestCase):

    # Test for addition of two positive numbers
    def test_add_positive_numbers(self):
        result = add(3, 5)
        self.assertEqual(result, 8)

    # Test for addition of a positive and a negative number
    def test_add_positive_and_negative(self):
        result = add(10, -3)
        self.assertEqual(result, 7)

    # Test for addition of two negative numbers
    def test_add_negative_numbers(self):
        result = add(-5, -7)
        self.assertEqual(result, -12)

# Running the tests
if __name__ == '__main__':
    unittest.main()
