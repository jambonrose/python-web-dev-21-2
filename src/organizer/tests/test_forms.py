"""Tests for all forms in the Organizer app"""
from django.test import TestCase

from config.test_utils import get_instance_data, omit_keys

from ..forms import NewsLinkForm, StartupForm, TagForm
from ..models import NewsLink, Startup, Tag
from .factories import (
    NewsLinkFactory,
    StartupFactory,
    TagFactory,
)


class TagFormTests(TestCase):
    """Tests for TagForm"""

    def test_creation(self):
        """Can we save new tags based on input?"""
        self.assertFalse(
            Tag.objects.filter(name="django").exists()
        )
        bounded_form = TagForm(data=dict(name="Django"))
        self.assertTrue(
            bounded_form.is_valid(), bounded_form.errors
        )
        bounded_form.save()
        self.assertTrue(
            Tag.objects.filter(name="django").exists()
        )

    # AutoSlugField does not have a field in ModelForms!
    # def test_slug_validation(self):
    #     """Do we error if slug is create?"""
    #     tform = TagForm(
    #         data=dict(name="django", slug="create")
    #     )
    #     self.assertFalse(tform.is_valid())

    def test_update(self):
        """Can we save new tags based on input?"""
        tag = TagFactory()
        self.assertNotEqual(tag.name, "django")
        tform = TagForm(
            data=dict(name="Django"), instance=tag
        )
        self.assertTrue(tform.is_valid(), tform.errors)
        tform.save()
        tag.refresh_from_db()
        self.assertEqual(tag.name, "django")


class StartupFormTests(TestCase):
    """Tests for StartupForm"""

    def test_creation(self):
        """Can we save new startups based on input?"""
        tag = TagFactory()
        startup = StartupFactory.build()
        self.assertFalse(
            Startup.objects.filter(
                slug=startup.slug
            ).exists()
        )
        bounded_form = StartupForm(
            data={
                **get_instance_data(startup),
                "tags": [tag.pk],
            }
        )
        self.assertTrue(
            bounded_form.is_valid(), bounded_form.errors
        )
        bounded_form.save()
        self.assertTrue(
            Startup.objects.filter(
                slug=startup.slug
            ).exists()
        )

    def test_slug_validation(self):
        """Do we error if slug is create?"""
        data = omit_keys(
            "slug",
            get_instance_data(StartupFactory.build()),
        )
        sform = StartupForm({**data, "slug": "create"})
        self.assertFalse(sform.is_valid())

    def test_update(self):
        """Can we updated startups based on input?"""
        tag = TagFactory()
        startup = StartupFactory(tags=[tag])
        self.assertNotEqual(startup.name, "django")
        sform = StartupForm(
            instance=startup,
            data=dict(
                omit_keys(
                    "name", get_instance_data(startup)
                ),
                name="django",
                tags=[tag.pk],
            ),
        )
        self.assertTrue(sform.is_valid(), sform.errors)
        sform.save()
        startup.refresh_from_db()
        self.assertEqual(startup.name, "django")


class NewsLinkFormTests(TestCase):
    """Tests for NewsLinkForm"""

    def test_creation(self):
        """Can we save new newslinks based on input?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory.build()
        self.assertFalse(
            NewsLink.objects.filter(
                slug=newslink.slug
            ).exists()
        )
        bounded_form = NewsLinkForm(
            data={
                **get_instance_data(newslink),
                "startup": startup.pk,
            }
        )
        self.assertTrue(
            bounded_form.is_valid(), bounded_form.errors
        )
        bounded_form.save()
        self.assertTrue(
            NewsLink.objects.filter(
                slug=newslink.slug
            ).exists()
        )

    def test_update(self):
        """Can we updated newslinks based on input?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory(startup=startup)
        self.assertNotEqual(newslink.title, "django")
        nl_form = NewsLinkForm(
            instance=newslink,
            data=dict(
                omit_keys(
                    "name", get_instance_data(newslink)
                ),
                title="django",
                startups=[startup.pk],
            ),
        )
        self.assertTrue(nl_form.is_valid(), nl_form.errors)
        nl_form.save()
        newslink.refresh_from_db()
        self.assertEqual(newslink.title, "django")

    def test_slug_validation(self):
        """Do we error if slug conflicts with URL?"""
        conflicts = ["delete", "update", "add_article"]
        startup = StartupFactory()
        for url_path in conflicts:
            with self.subTest(slug=url_path):
                nl_form = NewsLinkForm(
                    dict(
                        get_instance_data(
                            NewsLinkFactory.build()
                        ),
                        slug=url_path,
                        startup=startup.pk,
                    )
                )
                self.assertFalse(nl_form.is_valid())
