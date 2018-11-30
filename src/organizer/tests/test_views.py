"""Tests for (traditional/HTML) views for Organizer App"""
from random import randint

from django.utils.text import slugify
from test_plus import TestCase

from config.test_utils import (
    get_instance_data,
    omit_keys,
    reverse,
)

from ..forms import NewsLinkForm, StartupForm, TagForm
from ..models import NewsLink, Startup, Tag
from .factories import (
    NewsLinkFactory,
    StartupFactory,
    TagFactory,
)


class TagViewTests(TestCase):
    """Tests for views that return Tags in HTML"""

    def test_tag_list(self):
        """Do we render lists of tags?"""
        tag_list = TagFactory.create_batch(5)
        self.get_check_200("tag_list")
        self.assertInContext("tag_list")
        self.assertCountEqual(
            self.get_context("tag_list"), tag_list
        )
        self.assertTemplateUsed(
            self.last_response, "tag/list.html"
        )
        self.assertTemplateUsed(
            self.last_response, "tag/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_tag_list_empty(self):
        """Do we render lists of tags if no tags?"""
        self.get_check_200("tag_list")
        self.assertInContext("tag_list")
        self.assertCountEqual(
            self.get_context("tag_list"), []
        )
        self.assertTemplateUsed(
            self.last_response, "tag/list.html"
        )
        self.assertTemplateUsed(
            self.last_response, "tag/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_tag_detail(self):
        """Do we render details of a tag?"""
        tag = TagFactory()
        self.get_check_200("tag_detail", slug=tag.slug)
        self.assertContext("tag", tag)
        self.assertTemplateUsed(
            self.last_response, "tag/detail.html"
        )
        self.assertTemplateUsed(
            self.last_response, "tag/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_tag_detail_404(self):
        """Do we return 404 for missing Tags?"""
        self.get("tag_detail", slug="nonexistent")
        self.response_404()

    def test_tag_create_get(self):
        """Can we view a form to create Tags?"""
        response = self.get_check_200("tag_create")
        form = self.get_context("form")
        self.assertIsInstance(form, TagForm)
        self.assertContext("update", False)
        self.assertTemplateUsed(response, "tag/form.html")
        self.assertTemplateUsed(response, "tag/base.html")
        self.assertTemplateUsed(response, "base.html")

    def test_tag_create_post(self):
        """Can we submit a form to create tags?"""
        self.assertEqual(Tag.objects.count(), 0)
        tag_data = omit_keys(
            "id", get_instance_data(TagFactory.build())
        )
        response = self.post("tag_create", data=tag_data)
        self.assertEqual(
            Tag.objects.count(), 1, response.content
        )
        tag = Tag.objects.get(
            slug=slugify(tag_data["name"])
        )
        self.assertRedirects(
            response, tag.get_absolute_url()
        )

    def test_tag_update_get(self):
        """Can we view a form to update Tags?"""
        tag = TagFactory()
        response = self.get_check_200(
            "tag_update", slug=tag.slug
        )
        form = self.get_context("form")
        self.assertIsInstance(form, TagForm)
        context_tag = self.get_context("tag")
        self.assertEqual(tag.pk, context_tag.pk)
        self.assertContext("update", True)
        self.assertTemplateUsed(response, "tag/form.html")
        self.assertTemplateUsed(response, "tag/base.html")
        self.assertTemplateUsed(response, "base.html")

    def test_tag_update_post(self):
        """Can we submit a form to update tags?"""
        tag = TagFactory()
        self.assertNotEqual(tag.name, "django")
        tag_data = omit_keys(
            "id", "name", get_instance_data(tag)
        )
        response = self.post(
            "tag_update",
            slug=tag.slug,
            data=dict(**tag_data, name="django"),
        )
        tag.refresh_from_db()
        self.assertEqual(
            tag.name, "django", response.content
        )
        self.assertRedirects(
            response, tag.get_absolute_url()
        )

    def test_tag_delete_get(self):
        """Can we view a form to delete a Tag?"""
        tag = TagFactory()
        response = self.get_check_200(
            "tag_delete", slug=tag.slug
        )
        context_tag = self.get_context("tag")
        self.assertEqual(tag.pk, context_tag.pk)
        self.assertTemplateUsed(
            response, "tag/confirm_delete.html"
        )
        self.assertTemplateUsed(response, "tag/base.html")
        self.assertTemplateUsed(response, "base.html")

    def test_tag_delete_post(self):
        """Can we submit a form to delete a Tag?"""
        tag = TagFactory()
        response = self.post("tag_delete", slug=tag.slug)
        self.assertRedirects(response, reverse("tag_list"))
        self.assertFalse(
            Tag.objects.filter(slug=tag.slug).exists()
        )


class StartupViewTests(TestCase):
    """Tests for views that return Startups in HTML"""

    def test_startup_list(self):
        """Do we render lists of startups?"""
        startup_list = StartupFactory.create_batch(5)
        self.get_check_200("startup_list")
        self.assertInContext("startup_list")
        self.assertCountEqual(
            self.get_context("startup_list"), startup_list
        )
        self.assertTemplateUsed(
            self.last_response, "startup/list.html"
        )
        self.assertTemplateUsed(
            self.last_response, "startup/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_startup_list_empty(self):
        """Do we render lists of startups if no startups?"""
        self.get_check_200("startup_list")
        self.assertInContext("startup_list")
        self.assertCountEqual(
            self.get_context("startup_list"), []
        )
        self.assertTemplateUsed(
            self.last_response, "startup/list.html"
        )
        self.assertTemplateUsed(
            self.last_response, "startup/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_startup_detail(self):
        """Do we render details of a startup?"""
        startup = StartupFactory()
        self.get_check_200(
            "startup_detail", slug=startup.slug
        )
        self.assertContext("startup", startup)
        self.assertTemplateUsed(
            self.last_response, "startup/detail.html"
        )
        self.assertTemplateUsed(
            self.last_response, "startup/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_startup_detail_404(self):
        """Do we return 404 for missing Startups?"""
        self.get("startup_detail", slug="nonexistent")
        self.response_404()

    def test_create_get(self):
        """Can we view the form to create Startups?"""
        response = self.get_check_200("startup_create")
        form = self.get_context("form")
        self.assertIsInstance(form, StartupForm)
        self.assertContext("update", False)
        self.assertTemplateUsed(
            response, "startup/form.html"
        )
        self.assertTemplateUsed(
            response, "startup/base.html"
        )
        self.assertTemplateUsed(response, "base.html")

    def test_create_post(self):
        """Can we submit a form to create Startups?"""
        startup_num = Startup.objects.count()
        tag = TagFactory()
        startup_data = {
            **omit_keys(
                "id",
                get_instance_data(StartupFactory.build()),
            ),
            "tags": [tag.pk],
        }
        response = self.post(
            "startup_create", data=startup_data
        )
        self.assertEqual(
            Startup.objects.count(),
            startup_num + 1,
            response.content.decode("utf8"),
        )
        startup = Startup.objects.get(
            slug=startup_data["slug"]
        )
        self.assertIn(tag, startup.tags.all())
        self.assertRedirects(
            response, startup.get_absolute_url()
        )

    def test_update_get(self):
        """Can we view a form to update startups?"""
        startup = StartupFactory()
        response = self.get_check_200(
            "startup_update", slug=startup.slug
        )
        form = self.get_context("form")
        self.assertIsInstance(form, StartupForm)
        context_startup = self.get_context("startup")
        self.assertEqual(startup.pk, context_startup.pk)
        self.assertContext("update", True)
        self.assertTemplateUsed(
            response, "startup/form.html"
        )
        self.assertTemplateUsed(
            response, "startup/base.html"
        )
        self.assertTemplateUsed(response, "base.html")

    def test_update_post(self):
        """Can we submit a form to update startups?"""
        startup = StartupFactory(
            tags=TagFactory.create_batch(randint(1, 5))
        )
        self.assertNotEqual(startup.name, "django")
        startup_data = omit_keys(
            "id", get_instance_data(startup)
        )
        response = self.post(
            "startup_update",
            slug=startup.slug,
            data=dict(startup_data, name="django"),
        )
        startup.refresh_from_db()
        self.assertEqual(
            startup.name,
            "django",
            response.content.decode("utf8"),
        )
        self.assertRedirects(
            response, startup.get_absolute_url()
        )

    def test_delete_get(self):
        """Can we view a form to delete a Startup?"""
        startup = StartupFactory()
        response = self.get_check_200(
            "startup_delete", slug=startup.slug
        )
        context_startup = self.get_context("startup")
        self.assertEqual(startup.pk, context_startup.pk)
        self.assertTemplateUsed(
            response, "startup/confirm_delete.html"
        )
        self.assertTemplateUsed(
            response, "startup/base.html"
        )
        self.assertTemplateUsed(response, "base.html")

    def test_delete_post(self):
        """Can we submit a form to delete a Startup?"""
        startup = StartupFactory()
        response = self.post(
            "startup_delete", slug=startup.slug
        )
        self.assertRedirects(
            response, reverse("startup_list")
        )
        self.assertFalse(
            Startup.objects.filter(pk=startup.pk).exists()
        )


class NewsLinkViewTests(TestCase):
    """Tests for views that return NewsLinks in HTML"""

    def test_startup_redirect(self):
        """Does URI with both slugs redirect to Startup page?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory(startup=startup)
        response = self.get(
            "newslink_detail",
            startup_slug=startup.slug,
            newslink_slug=newslink.slug,
        )
        self.assertRedirects(
            response, startup.get_absolute_url()
        )

    def test_create_get(self):
        """Can we view the form to create NewsLinks?"""
        startup = StartupFactory()
        response = self.get_check_200(
            "newslink_create", startup_slug=startup.slug
        )
        form = self.get_context("form")
        self.assertIsInstance(form, NewsLinkForm)
        context_startup = self.get_context("startup")
        self.assertEqual(startup.pk, context_startup.pk)
        self.assertContext("update", False)
        self.assertTemplateUsed(
            response, "newslink/form.html"
        )
        self.assertTemplateUsed(
            response, "newslink/base.html"
        )
        self.assertTemplateUsed(response, "base.html")

    def test_create_post(self):
        """Can we submit a form to create NewsLinks?"""
        newslink_num = NewsLink.objects.count()
        startup = StartupFactory()
        newslink_data = {
            **omit_keys(
                "id",
                get_instance_data(NewsLinkFactory.build()),
            ),
            "startup": startup.pk,
        }
        response = self.post(
            "newslink_create",
            startup_slug=startup.slug,
            data=newslink_data,
        )
        self.assertEqual(
            NewsLink.objects.count(),
            newslink_num + 1,
            response.content.decode("utf8"),
        )
        newslink = NewsLink.objects.get(
            slug=newslink_data["slug"]
        )
        self.assertEqual(startup.pk, newslink.startup.pk)
        self.assertRedirects(
            response, newslink.get_absolute_url()
        )

    def test_update_get(self):
        """Can we view a form to update newslinks?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory(startup=startup)
        response = self.get_check_200(
            "newslink_update",
            startup_slug=startup.slug,
            newslink_slug=newslink.slug,
        )
        form = self.get_context("form")
        self.assertIsInstance(form, NewsLinkForm)
        context_newslink = self.get_context("newslink")
        context_startup = self.get_context("startup")
        self.assertEqual(newslink.pk, context_newslink.pk)
        self.assertEqual(startup.pk, context_startup.pk)
        self.assertContext("update", True)
        self.assertTemplateUsed(
            response, "newslink/form.html"
        )
        self.assertTemplateUsed(
            response, "newslink/base.html"
        )
        self.assertTemplateUsed(response, "base.html")

    def test_update_post(self):
        """Can we submit a form to update newslinks?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory(startup=startup)
        self.assertNotEqual(newslink.title, "django")
        newslink_data = omit_keys(
            "id", get_instance_data(newslink)
        )
        response = self.post(
            "newslink_update",
            startup_slug=startup.slug,
            newslink_slug=newslink.slug,
            data=dict(newslink_data, title="django"),
        )
        newslink.refresh_from_db()
        self.assertEqual(
            newslink.title,
            "django",
            response.content.decode("utf8"),
        )
        self.assertRedirects(
            response, newslink.get_absolute_url()
        )

    def test_delete_get(self):
        """Can we view a form to delete a NewsLink?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory(startup=startup)
        response = self.get_check_200(
            "newslink_delete",
            startup_slug=startup.slug,
            newslink_slug=newslink.slug,
        )
        context_newslink = self.get_context("newslink")
        context_startup = self.get_context("startup")
        self.assertEqual(newslink.pk, context_newslink.pk)
        self.assertEqual(startup.pk, context_startup.pk)
        self.assertTemplateUsed(
            response, "newslink/confirm_delete.html"
        )
        self.assertTemplateUsed(
            response, "newslink/base.html"
        )
        self.assertTemplateUsed(response, "base.html")

    def test_delete_post(self):
        """Can we submit a form to delete a NewsLink?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory(startup=startup)
        response = self.post(
            "newslink_delete",
            startup_slug=startup.slug,
            newslink_slug=newslink.slug,
        )
        self.assertRedirects(
            response, startup.get_absolute_url()
        )
        self.assertFalse(
            NewsLink.objects.filter(pk=newslink.pk).exists()
        )
