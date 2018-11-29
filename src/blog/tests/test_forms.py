"""Tests for all forms in the Organizer app"""
from django.test import TestCase

from config.test_utils import get_instance_data
from organizer.tests.factories import (
    StartupFactory,
    TagFactory,
)

from ..forms import PostForm
from ..models import Post
from .factories import PostFactory


class PostFormTests(TestCase):
    """Tests for PostForm"""

    def test_creation(self):
        """Can we save new posts based on input?"""
        tag = TagFactory()
        startup = StartupFactory()
        post = PostFactory.build()
        self.assertFalse(
            Post.objects.filter(slug=post.slug).exists()
        )
        bounded_form = PostForm(
            data={
                **get_instance_data(post),
                "tags": [tag.pk],
                "startups": [startup.pk],
            }
        )
        self.assertTrue(
            bounded_form.is_valid(), bounded_form.errors
        )
        bounded_form.save()
        self.assertTrue(
            Post.objects.filter(slug=post.slug).exists()
        )

    def test_update(self):
        """Can we update posts based on input?"""
        tag = TagFactory()
        startup = StartupFactory()
        post = PostFactory(tags=[tag], startups=[startup])
        self.assertNotEqual(post.title, "django")
        pform = PostForm(
            instance=post,
            data=dict(
                get_instance_data(post),
                title="django",
                tags=[tag.pk],
                startups=[startup.pk],
            ),
        )
        self.assertTrue(pform.is_valid(), pform.errors)
        pform.save()
        post.refresh_from_db()
        self.assertEqual(post.title, "django")
