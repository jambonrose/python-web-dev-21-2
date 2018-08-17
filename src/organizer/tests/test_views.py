"""Tests for (traditional/HTML) views for Organizer App"""
from test_plus import TestCase

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
