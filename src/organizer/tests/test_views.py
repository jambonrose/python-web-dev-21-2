"""Tests for (traditional/HTML) views for Organizer App"""
from test_plus import TestCase

from .factories import TagFactory


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
