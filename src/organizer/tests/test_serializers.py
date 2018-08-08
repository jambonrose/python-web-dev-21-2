"""Tests for Serializers in the Organizer App"""
from django.test import TestCase

from config.test_utils import (
    get_instance_data,
    lmap,
    omit_keys,
)

from ..serializers import StartupSerializer, TagSerializer
from .factories import StartupFactory, TagFactory


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


class StartupSerializerTests(TestCase):
    """Test Serialization of Startups in StartupSerializer"""

    def test_serialization(self):
        """Does an existing Startup serialize correctly?"""
        tag_list = TagFactory.create_batch(3)
        startup = StartupFactory(tags=tag_list)
        s_startup = StartupSerializer(startup)
        self.assertEqual(
            omit_keys("tags", s_startup.data),
            omit_keys("tags", get_instance_data(startup)),
        )
        self.assertCountEqual(
            s_startup.data["tags"],
            TagSerializer(tag_list, many=True).data,
        )

    def test_deserialization(self):
        """Can we deserialize data to a Startup model?"""
        startup_data = get_instance_data(
            StartupFactory.build()
        )
        tag_dicts = lmap(
            get_instance_data, TagFactory.build_batch(3)
        )
        data = dict(startup_data, tags=tag_dicts)
        s_startup = StartupSerializer(data=data)
        self.assertTrue(
            s_startup.is_valid(), msg=s_startup.errors
        )

    def test_invalid_deserialization(self):
        """Does the serializer validate data?"""
        s_startup = StartupSerializer(data={})
        self.assertFalse(s_startup.is_valid())
