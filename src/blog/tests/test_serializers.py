"""Tests for Serializers in the Blog App"""
from functools import partial

from django.test import TestCase

from config.test_utils import (
    context_kwarg,
    get_instance_data,
    lmap,
    omit_keys,
    reverse,
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
        post_ctxt = context_kwarg(
            f"/api/v1/startup/{post.slug}"
        )
        s_post = PostSerializer(post, **post_ctxt)
        self.assertEqual(
            remove_m2m("url", s_post.data),
            remove_m2m("id", get_instance_data(post)),
        )
        self.assertEqual(
            s_post.data["url"],
            reverse(
                "api-post-detail",
                year=post.pub_date.year,
                month=post.pub_date.month,
                slug=post.slug,
                full=True,
            ),
        )
        self.assertCountEqual(
            s_post.data["tags"],
            TagSerializer(
                tag_list, many=True, **post_ctxt
            ).data,
        )
        self.assertCountEqual(
            s_post.data["startups"],
            StartupSerializer(
                startup_list, many=True, **post_ctxt
            ).data,
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
        s_post = PostSerializer(
            data=data, **context_kwarg(f"/api/v1/startup/")
        )
        self.assertTrue(
            s_post.is_valid(), msg=s_post.errors
        )

    def test_invalid_deserialization(self):
        """Does the serializer validate data?"""
        s_post = PostSerializer(data={})
        self.assertFalse(s_post.is_valid())
