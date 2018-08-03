"""Test for blog app"""
from django.test import TestCase

from config.test_utils import get_concrete_field_names

from ..models import NewsLink, Startup, Tag


class TagModelTests(TestCase):
    """Tests for the Tag model"""

    def test_concrete_fields(self):
        """Do we find the expected fields on the Tag model?"""
        field_names = get_concrete_field_names(Tag)
        expected_field_names = ["id", "name", "slug"]
        self.assertEqual(field_names, expected_field_names)


class StartupModelTests(TestCase):
    """Tests for the Startup model"""

    def test_concrete_fields(self):
        """Do we find the expected fields on the Startup model?"""
        field_names = get_concrete_field_names(Startup)
        expected_field_names = [
            "id",
            "name",
            "slug",
            "description",
            "founded_date",
            "contact",
            "website",
        ]
        self.assertEqual(field_names, expected_field_names)


class NewsLinkModelTests(TestCase):
    """Tests for the NewsLink model"""

    def test_concrete_fields(self):
        """Do we find the expected fields on the NewsLink model?"""
        field_names = get_concrete_field_names(NewsLink)
        expected_field_names = [
            "id",
            "title",
            "slug",
            "pub_date",
            "link",
        ]
        self.assertEqual(field_names, expected_field_names)
