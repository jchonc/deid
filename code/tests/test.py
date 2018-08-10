"""Tests"""
import unittest
from .context import deid

class DeIdentificationTestSuite(unittest.TestCase):
    """The normal test cases"""

    def test_can_call(self):
        """Something is working"""
        assert True

    def test_can_call_func(self):
        """Call to lib is working"""
        result = deid.lib.de_identify_text("abcdefg")
        self.assertEqual(result, "abcdefg")

if __name__ == '__main__':
    unittest.main()
