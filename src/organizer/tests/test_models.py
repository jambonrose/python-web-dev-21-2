"""Test for blog app"""
from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from blog.models import Post
from blog.tests.factories import PostFactory
from config.test_utils import (
    get_concrete_field_names,
    reverse,
)

from ..models import NewsLink, Startup, Tag
from .factories import (
    NewsLinkFactory,
    StartupFactory,
    TagFactory,
)


class TagModelTests(TestCase):
    """Tests for the Tag model"""

    def test_concrete_fields(self):
        """Do we find the expected fields on the Tag model?"""
        field_names = get_concrete_field_names(Tag)
        expected_field_names = ["id", "name", "slug"]
        self.assertEqual(field_names, expected_field_names)

    def test_name_uniqueness(self):
        """Are Tags with identical names disallowed?"""
        kwargs = dict(name="a")
        TagFactory(**kwargs)
        with self.assertRaises(IntegrityError):
            TagFactory(**kwargs)

    def test_slug_uniqueness(self):
        """Are Tags generated with unique slugs?

        This test is a little tricky. We need to force the system to
        generate the same slug based on distinct values. Thankfully, we
        know that slugs have spaces removed, so we can rely on this to
        create Tags named 'a ' and ' a'. These should thus both generate
        a slug 'a'. The second to be generated will need to generate a
        different value, however, as the first will have already taken
        the slug 'a'.
        """
        t1 = Tag.objects.create(name="a ")
        t2 = Tag.objects.create(name=" a")
        self.assertEqual("a", t1.slug)
        self.assertEqual("a-2", t2.slug)

    def test_list_order(self):
        """Are tags ordered by name?

        This test is actually dependent on the database and whether the
        field is unique. In SQLite3, the order will be alphabetical if
        the name field is unique.

        Will pass regardless if/once Meta ordering is defined.

        """
        TagFactory(name="b")
        TagFactory(name="D")
        TagFactory(name="c")
        TagFactory(name="a")
        tag_name_list = list(
            Tag.objects.values_list("name", flat=True)
        )
        expected_name_list = ["D", "a", "b", "c"]
        self.assertEqual(tag_name_list, expected_name_list)

    def test_str(self):
        """Do Tags clearly represent themselves?"""
        t = TagFactory(name="django")
        self.assertEqual(str(t), "django")

    def test_absolute_url(self):
        """Do Tags link to their detail view?"""
        tag = TagFactory()
        self.assertEqual(
            tag.get_absolute_url(),
            reverse("tag_detail", slug=tag.slug),
        )

    def test_delete(self):
        """Does deleting a Tag leave related objects?"""
        tag = TagFactory()
        startups = StartupFactory.create_batch(
            3, tags=[tag]
        )
        posts = PostFactory.create_batch(
            3, tags=[tag], startups=startups
        )

        self.assertEqual(
            Post.objects.count(),
            3,
            "Unexpected initial condition",
        )
        self.assertEqual(
            Startup.objects.count(),
            3,
            "Unexpected initial condition",
        )
        self.assertEqual(posts[0].tags.all()[0].pk, tag.pk)
        self.assertEqual(
            startups[0].tags.all()[0].pk, tag.pk
        )

        tag.delete()

        self.assertEqual(
            Post.objects.count(), 3, "Unexpected change"
        )
        self.assertEqual(
            Startup.objects.count(), 3, "Unexpected change"
        )


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

    def test_slug_uniqueness(self):
        """Are Startups with identical slugs disallowed?"""
        kwargs = dict(slug="a")
        StartupFactory(**kwargs)
        with self.assertRaises(IntegrityError):
            StartupFactory(**kwargs)

    def test_list_order(self):
        """Are Startups ordered by name?

        This test is actually dependent on the database and whether the
        field is unique. In SQLite3, the order will be alphabetical if
        the name field is unique.

        Will pass regardless if/once Meta ordering is defined.

        """
        StartupFactory(name="b")
        StartupFactory(name="D")
        StartupFactory(name="c")
        StartupFactory(name="a")
        startup_name_list = list(
            Startup.objects.values_list("name", flat=True)
        )
        expected_name_list = ["D", "a", "b", "c"]
        self.assertEqual(
            startup_name_list, expected_name_list
        )

    def test_tag_m2m(self):
        """Do Startups have Many-To-Many Tags?

        https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-attribute-reference

        Let's have fun with this one! This is not how you'd write this test
        normally, but it does demonstrate some interesting field properties.

        """
        tags_field = Startup._meta.get_field("tags")
        # check nature of field
        self.assertFalse(tags_field.auto_created)
        self.assertTrue(tags_field.is_relation)
        self.assertTrue(tags_field.many_to_many)
        self.assertIs(tags_field.related_model, Tag)
        # the checks below are technically redundant
        self.assertTrue(tags_field.concrete)
        self.assertFalse(tags_field.one_to_one)
        self.assertFalse(tags_field.one_to_many)
        self.assertFalse(tags_field.many_to_one)

    def test_startup_str(self):
        """Do Startups clearly represent themselves?"""
        t = StartupFactory(name="JamBon")
        self.assertEqual(str(t), "JamBon")

    def test_absolute_url(self):
        """Do Startups link to their detail view?"""
        startup = StartupFactory()
        self.assertEqual(
            startup.get_absolute_url(),
            reverse("startup_detail", slug=startup.slug),
        )

    def test_delete(self):
        """Does deleting a startup leave tags alone?"""
        tags = TagFactory.create_batch(2)
        startup = StartupFactory(tags=tags)

        self.assertEqual(
            Tag.objects.count(),
            2,
            "Unexpected initial condition",
        )
        self.assertIn(
            tags[0],
            startup.tags.all(),
            "Unexpected initial condition",
        )

        startup.delete()

        self.assertEqual(
            Tag.objects.count(), 2, "Unexpected change"
        )

    def test_get_latest(self):
        """Can managers get the youngest Startup?"""
        StartupFactory(
            name="b", founded_date=date(2017, 1, 1)
        )
        StartupFactory(
            name="d", founded_date=date(2016, 1, 1)
        )
        latest = StartupFactory(
            name="z", founded_date=date(2018, 1, 1)
        )
        found = Startup.objects.latest()
        self.assertEqual(found, latest)


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

    def test_newslink_startup_fk(self):
        """Does NewsLink have a Foreign Key to Startup?

        https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-attribute-reference

        Let's have fun with this one! This is not how you'd write this test
        normally, but it does demonstrate some interesting field properties.

        """
        startup_field = NewsLink._meta.get_field("startup")
        # check nature of field
        self.assertFalse(startup_field.auto_created)
        self.assertTrue(startup_field.is_relation)
        self.assertTrue(startup_field.many_to_one)
        self.assertIs(startup_field.related_model, Startup)
        # the checks below are technically redundant
        self.assertTrue(startup_field.concrete)
        self.assertFalse(startup_field.one_to_one)
        self.assertFalse(startup_field.one_to_many)
        self.assertFalse(startup_field.many_to_many)

    def test_str(self):
        """Do articles clearly represent themselves?"""
        s = StartupFactory(name="JamBon")
        nl = NewsLinkFactory(
            title="consult and teach!", startup=s
        )
        self.assertEqual(
            str(nl), "JamBon: consult and teach!"
        )

    def test_uniqueness(self):
        """Are articles for a startup unique by slug?"""
        s = StartupFactory(name="JamBon")
        kwargs = dict(slug="new", startup=s)
        NewsLinkFactory(**kwargs)
        with self.assertRaises(IntegrityError):
            NewsLinkFactory(**kwargs)

    def test_delete(self):
        """Does deleting a NewsLink leave the Startup?"""
        s = StartupFactory()
        nl = NewsLinkFactory(startup=s)

        self.assertEqual(s.pk, nl.startup.pk)
        self.assertEqual(
            Startup.objects.count(),
            1,
            "Unexpected initial condition",
        )

        nl.delete()

        self.assertEqual(
            Startup.objects.count(), 1, "Unexpected change"
        )
