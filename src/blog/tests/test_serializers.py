"""Tests for Serializers in the Blog App"""
from functools import partial

from django.test import TestCase

from config.test_utils import (
    get_instance_data,
    lmap,
    omit_keys,
)
from organizer.serializers import (
    StartupSerializer,
    TagSerializer,
)
from organizer.tests.factories import (
    StartupFactory,
    TagFactory,
)

from ..serializers import PostSerializer
from .factories import PostFactory

remove_m2m = partial(omit_keys, "tags", "startups")


class PostSerializerTests(TestCase):
    """Test Serialization of Blog Posts in PostSerializer"""

    maxDiff = None

    def test_serialization(self):
        """Does an existing Posts serialize correctly?"""
        tag_list = TagFactory.create_batch(3)
        startup_list = StartupFactory.create_batch(2)
        post = PostFactory(
            tags=tag_list, startups=startup_list
        )
        s_post = PostSerializer(post)
        self.assertEqual(
            remove_m2m(s_post.data),
            remove_m2m(get_instance_data(post)),
        )
        self.assertCountEqual(
            s_post.data["tags"],
            TagSerializer(tag_list, many=True).data,
        )
        self.assertCountEqual(
            s_post.data["startups"],
            StartupSerializer(startup_list, many=True).data,
        )

    def test_deserialization(self):
        """Can we deserialize data to a Post model?"""
        tag_dicts = lmap(
            get_instance_data, TagFactory.build_batch(2)
        )
        startup_tag_dicts = lmap(
            get_instance_data, TagFactory.build_batch(2)
        )
        startup_data = remove_m2m(
            get_instance_data(StartupFactory.build())
        )
        post_data = remove_m2m(
            get_instance_data(PostFactory.build())
        )
        data = dict(
            **post_data,
            tags=tag_dicts,
            startups=[
                {**startup_data, "tags": startup_tag_dicts}
            ],
        )
        s_post = PostSerializer(data=data)
        self.assertTrue(
            s_post.is_valid(), msg=s_post.errors
        )

    def test_invalid_deserialization(self):
        """Does the serializer validate data?"""
        s_post = PostSerializer(data={})
        self.assertFalse(s_post.is_valid())
