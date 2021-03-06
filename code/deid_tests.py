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

    def test_can_redact_person_name(self):
        """Mask the name of a person"""
        result = self.handler.process_text("Lucas Zhou had a sandwich for breakfast at 8 AM.")
        self.assertEqual(result.find('Lucas Zhou'), -1)
       
    def test_can_redact_date(self):
        """A date string need to be redacted"""
        result = self.handler.process_text("Harry Potter went home on 12-11-2017.")
        self.assertEqual(result.find('12-11-2017'), -1)

    def test_can_redact_time(self):
        """Verify time information could be redacted"""
        result = self.handler.process_text("Harry Potter went home at 12:30 PM.")
        self.assertEqual(result.find('12:30 PM'), -1)
    
    def test_can_redact_telephone(self):
        """Telephone information needs to be masked"""
        result = self.handler.process_text("Patient called from (213)222-3333 this morning to cancel the appointment.")
        self.assertEqual(result.find('(213)222-3333'), -1)
    
    def test_can_redact_email(self):
        """Email information needs to be masked"""
        result = self.handler.process_text("Patient emailed from jszxv@gmail.com this morning to cancel the appointment.")
        self.assertEqual(result.find('jszxv@gmail.com'), -1)

    def test_can_redact_url(self):
        """URL information needs to be masked"""
        result = self.handler.process_text("Patient visited http://www.abc.com/somewhere-something/a%20/a.jpg this morning to cancel the appointment.")
        self.assertEqual(result.find('http://www.abc.com'), -1)

    def test_can_redact_ip(self):
        """IP information needs to be masked"""
        result = self.handler.process_text("Employee from workstation 10.5.6.210 called this morning to cancel the appointment.")
        self.assertEqual(result.find('10.5.6.210'), -1)

    def test_can_normalize_html(self):
        """can extra pure text from HTML mixture"""
        input = """<div>this&nbsp;<span>is</span>&nbsp;an <span>apple</span></div>"""
        result = self.handler.normalize_text(input)
        self.assertEqual(result.find("<"), -1)

    def test_can_match_ids(self):
        """some various ids"""
        possible_ids = [
            "200625268", "#200625268", "B873A235C", "#B873A235C", 
            "12-0324AC", "#12-0324AC", "ACCB01-1234C", "#ACCB01-1234C"
        ]
        for case in possible_ids:
            input = "Dr. Smith has entered note in Johnson's chart MRN " + case
            result = self.handler.process_text(input)
            self.assertEqual(result.find(case), -1)


if __name__ == '__main__':
    unittest.main()
