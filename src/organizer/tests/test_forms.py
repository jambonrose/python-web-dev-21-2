"""Tests for all forms in the Organizer app"""
from django.test import TestCase

from ..forms import TagForm
from ..models import Tag


class TagFormTests(TestCase):
    """Tests for TagForm"""

    def test_creation(self):
        """Can we save new tags based on input?"""
        self.assertFalse(
            Tag.objects.filter(name="django").exists()
        )
        bounded_form = TagForm(data=dict(name="django"))
        self.assertTrue(
            bounded_form.is_valid(), bounded_form.errors
        )
        bounded_form.save()
        self.assertTrue(
            Tag.objects.filter(name="django").exists()
        )
