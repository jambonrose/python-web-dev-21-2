"""Tests for Serializers in the Organizer App"""
from django.test import TestCase

from config.test_utils import get_instance_data

from ..serializers import TagSerializer
from .factories import TagFactory


class TagSerializerTests(TestCase):
    """Test Serialization of Tags in TagSerializer"""

    def test_serialization(self):
        """Does an existing Tag serialize correctly?"""
        tag = TagFactory()
        s_tag = TagSerializer(tag)
        self.assertEqual(s_tag.data, get_instance_data(tag))

    def test_deserialization(self):
        """Can we deserialize data to a Tag model?"""
        tag_data = get_instance_data(TagFactory.build())
        s_tag = TagSerializer(data=tag_data)
        self.assertTrue(s_tag.is_valid(), s_tag.errors)

    def test_invalid_deserialization(self):
        """Does the serializer validate data?"""
        s_tag = TagSerializer(data={})
        self.assertFalse(s_tag.is_valid())
