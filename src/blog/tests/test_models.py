"""Test for blog app"""
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from config.test_utils import get_concrete_field_names
from organizer.models import Startup, Tag
from organizer.tests.factories import (
    StartupFactory,
    TagFactory,
)

from ..models import Post
from .factories import PostFactory


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

    def test_post_m2m_fields(self):
        """Are Posts Many-To-Many with Tags and Startups?"""
        post_m2m_fields = [
            field.name
            for field in Post._meta.get_fields()
            if not field.auto_created and field.many_to_many
        ]
        self.assertEqual(
            post_m2m_fields, ["tags", "startups"]
        )
        self.assertIs(
            Post._meta.get_field("tags").related_model, Tag
        )
        self.assertIs(
            Post._meta.get_field("startups").related_model,
            Startup,
        )

    def test_str(self):
        """Do Posts clearly represent themselves?"""
        p = PostFactory(
            title="b", pub_date=date(2017, 1, 1)
        )
        self.assertEqual(str(p), "b on 2017-01-01")

    def test_post_list_order(self):
        """Are posts ordered by date?"""
        PostFactory(title="b", pub_date=date(2017, 1, 1))
        PostFactory(title="a", pub_date=date(2016, 1, 1))
        PostFactory(title="a", pub_date=date(2017, 1, 1))
        PostFactory(title="d", pub_date=date(2018, 1, 1))
        post_name_list = [
            (name, p_date.year)
            for name, p_date in Post.objects.values_list(
                "title", "pub_date"
            )
        ]
        expected_name_list = [
            ("d", 2018),
            ("a", 2017),
            ("b", 2017),
            ("a", 2016),
        ]
        self.assertEqual(post_name_list, expected_name_list)

    def test_post_slug_uniqueness(self):
        """Are Posts with identical slugs in the same month disallowed?"""
        kwargs = dict(slug="a", pub_date=date(2018, 1, 1))
        PostFactory(**kwargs)
        with self.assertRaises(ValidationError):
            PostFactory.build(**kwargs).validate_unique()

    def test_get_latest(self):
        """Can managers get the latest Post?"""
        PostFactory(title="b", pub_date=date(2017, 1, 1))
        PostFactory(title="a", pub_date=date(2016, 1, 1))
        PostFactory(title="a", pub_date=date(2017, 1, 1))
        latest = PostFactory(
            title="d", pub_date=date(2018, 1, 1)
        )
        found = Post.objects.latest()
        self.assertEqual(latest, found)

    def test_delete(self):
        """Does deleting a post leave related objects?"""
        tags = TagFactory.create_batch(5)
        startups = StartupFactory.create_batch(3, tags=tags)
        post = PostFactory(tags=tags, startups=startups)

        self.assertIn(tags[0], post.tags.all())
        self.assertIn(startups[0], post.startups.all())
        self.assertEqual(
            Tag.objects.count(),
            5,
            "Unexpected initial condition",
        )
        self.assertEqual(
            Startup.objects.count(),
            3,
            "Unexpected initial condition",
        )

        post.delete()

        self.assertEqual(
            Tag.objects.count(), 5, "Unexpected change"
        )
        self.assertEqual(
            Startup.objects.count(), 3, "Unexpected change"
        )
