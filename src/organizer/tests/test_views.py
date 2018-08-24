"""Tests for (traditional/HTML) views for Organizer App"""
from django.utils.text import slugify
from test_plus import TestCase

from config.test_utils import (
    get_instance_data,
    omit_keys,
    reverse,
)

from ..forms import TagForm
from ..models import Tag
from .factories import StartupFactory, TagFactory


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
