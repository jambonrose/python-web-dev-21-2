"""Test for blog app"""
from django.test import TestCase

from config.test_utils import get_concrete_field_names

from ..models import Post


class PostModelTests(TestCase):
    """Tests for the Post model"""

    def test_post_concrete_fields(self):
        """Do we find the expected fields on the Post model?"""
        field_names = get_concrete_field_names(Post)
        expected_field_names = [
            "id",
            "title",
            "slug",
            "text",
            "pub_date",
        ]
        self.assertEqual(field_names, expected_field_names)
