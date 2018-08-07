"""Tests for Organizer Views"""
from test_plus import TestCase


class ViewTests(TestCase):
    """Basic class to test demo views"""

    def test_hello_world(self):
        """Is there a Hello World Example?"""
        self.get_check_200("hello_world")
