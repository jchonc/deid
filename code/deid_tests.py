"""Tests"""
import unittest
from . import lib

class DeIdentificationTest(unittest.TestCase):
    """The normal test cases"""

    def setUp(self):
        """Change lib to class?"""
        self.handler = lib.DeidentificationHandler()

    def tearDown(self):
        """Tear down"""
        self.handler = None

    def test_can_call(self):
        """Something is working"""

    def test_can_call_func(self):
        """Call to lib is working"""
        result = lib.de_identify_text("abcdefg")
        self.assertEqual(result, "abcdefg")

    def test_can_load_spacy(self):
        """First to get """
<<<<<<< HEAD
        result = self.handler.process_text("Lucas Zhou had a sandwich for breakfast at 8am.")
        self.assertTrue("Lucas Zhou" not in result)
        self.assertEqual(result, "abcd")
=======
        result = self.handler.process_text("Lucas Zhou had a sandwich for breakfast at 8AM.")
        self.assertEqual(result.find('Lucas Zhou'), -1)
>>>>>>> 629a3f052aab56eb00150fe52f047ccf02c3956a

if __name__ == '__main__':
    unittest.main()
