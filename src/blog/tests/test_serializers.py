"""Tests for Serializers in the Blog App"""
from functools import partial
from random import randint

from django.test import TestCase

from config.test_utils import (
    context_kwarg,
    get_instance_data,
    omit_keys,
    reverse,
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
            [
                reverse(
                    "api-tag-detail",
                    slug=tag.slug,
                    full=True,
                )
                for tag in tag_list
            ],
        )
        self.assertCountEqual(
            s_post.data["startups"],
            [
                reverse(
                    "api-startup-detail",
                    slug=startup.slug,
                    full=True,
                )
                for startup in startup_list
            ],
        )

    def test_deserialization(self):
        """Can we deserialize data to a Post model?"""
        tag_list = TagFactory.create_batch(randint(1, 10))
        tag_urls = [
            reverse("api-tag-detail", slug=tag.slug)
            for tag in tag_list
        ]
        startup_list = StartupFactory.create_batch(
            randint(1, 10)
        )
        startup_urls = [
            reverse("api-startup-detail", slug=startup.slug)
            for startup in startup_list
        ]
        post_data = remove_m2m(
            get_instance_data(PostFactory.build())
        )
        data = dict(
            **post_data,
            tags=tag_urls,
            startups=startup_urls,
        )
        s_post = PostSerializer(
            data=data,
            **context_kwarg(
                reverse("api-post-list", full=True)
            ),
        )
        self.assertTrue(
            s_post.is_valid(), msg=s_post.errors
        )
        post = s_post.save()
        self.assertCountEqual(tag_list, post.tags.all())
        self.assertCountEqual(
            startup_list, post.startups.all()
        )

    def test_deserialization_update(self):
        """Can we deserialize to an existing Post model?"""
        tag_list = TagFactory.create_batch(randint(1, 10))
        tag_urls = [
            reverse("api-tag-detail", slug=tag.slug)
            for tag in tag_list
        ]
        startup_list = StartupFactory.create_batch(
            randint(1, 10)
        )
        startup_urls = [
            reverse("api-startup-detail", slug=startup.slug)
            for startup in startup_list
        ]
        post = PostFactory(
            title="first", tags=TagFactory.create_batch(3)
        )
        post_data = remove_m2m(get_instance_data(post))
        data = dict(
            post_data,
            title="second",
            tags=tag_urls,
            startups=startup_urls,
        )
        s_post = PostSerializer(
            post,
            data=data,
            **context_kwarg(
                reverse(
                    "api-post-detail",
                    year=post.pub_date.year,
                    month=post.pub_date.month,
                    slug=post.slug,
                    full=True,
                )
            ),
        )
        self.assertTrue(
            s_post.is_valid(), msg=s_post.errors
        )
        post = s_post.save()
        self.assertEqual("second", post.title)
        self.assertCountEqual(tag_list, post.tags.all())
        self.assertCountEqual(
            startup_list, post.startups.all()
        )

    def test_deserialization_partial_update(self):
        """Can we partially deserialize data to a Post model?"""
        tag_list = TagFactory.create_batch(randint(1, 10))
        tag_urls = [
            reverse("api-tag-detail", slug=tag.slug)
            for tag in tag_list
        ]
        startup_list = StartupFactory.create_batch(
            randint(1, 10)
        )
        startup_urls = [
            reverse("api-startup-detail", slug=startup.slug)
            for startup in startup_list
        ]
        post = PostFactory(
            title="first", tags=TagFactory.create_batch(3)
        )
        s_post = PostSerializer(
            instance=post,
            data=dict(
                title="second",
                # necessary due to bug in DRF
                # https://github.com/encode/django-rest-framework/issues/6341
                slug=post.slug,
                pub_date=post.pub_date,
                # remove above once DRF fixed
                tags=tag_urls,
                startups=startup_urls,
            ),
            partial=True,
            **context_kwarg(
                reverse(
                    "api-post-detail",
                    year=post.pub_date.year,
                    month=post.pub_date.month,
                    slug=post.slug,
                    full=True,
                )
            ),
        )
        self.assertTrue(
            s_post.is_valid(), msg=s_post.errors
        )
        post = s_post.save()
        self.assertEqual("second", post.title)
        self.assertCountEqual(tag_list, post.tags.all())
        self.assertCountEqual(
            startup_list, post.startups.all()
        )

    def test_deserialization_partial_update_unknown_m2m(
        self
    ):
        """Can we partially deserialize data to a Post model?"""
        tag_urls = [
            reverse("api-tag-detail", slug=tag.slug)
            for tag in TagFactory.build_batch(
                randint(1, 10)
            )
        ]
        post = PostFactory()
        s_post = PostSerializer(
            instance=post,
            data=dict(
                # necessary due to bug in DRF
                # https://github.com/encode/django-rest-framework/issues/6341
                slug=post.slug,
                pub_date=post.pub_date,
                # remove above once DRF fixed
                tags=tag_urls,
            ),
            partial=True,
            **context_kwarg(
                reverse(
                    "api-post-detail",
                    year=post.pub_date.year,
                    month=post.pub_date.month,
                    slug=post.slug,
                    full=True,
                )
            ),
        )
        self.assertFalse(s_post.is_valid())

    def test_invalid_deserialization(self):
        """Does the serializer validate data?"""
        s_post = PostSerializer(data={})
        self.assertFalse(s_post.is_valid())
