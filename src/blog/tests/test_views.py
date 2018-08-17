"""Tests for (traditional/HTML) views for Organizer App"""
from test_plus import TestCase

from .factories import PostFactory


class PostViewTests(TestCase):
    """Tests for views that return Posts in HTML"""

    def test_post_list(self):
        """Do we render lists of posts?"""
        post_list = PostFactory.create_batch(5)
        self.get_check_200("post_list")
        self.assertInContext("post_list")
        self.assertCountEqual(
            self.get_context("post_list"), post_list
        )
        self.assertTemplateUsed(
            self.last_response, "post/list.html"
        )
        self.assertTemplateUsed(
            self.last_response, "post/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_post_list_empty(self):
        """Do we render lists of posts if no posts?"""
        self.get_check_200("post_list")
        self.assertInContext("post_list")
        self.assertCountEqual(
            self.get_context("post_list"), []
        )
        self.assertTemplateUsed(
            self.last_response, "post/list.html"
        )
        self.assertTemplateUsed(
            self.last_response, "post/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_post_detail(self):
        """Do we render details of a post?"""
        post = PostFactory()
        self.get_check_200(
            "post_detail",
            year=post.pub_date.year,
            month=post.pub_date.month,
            slug=post.slug,
        )
        self.assertContext("post", post)
        self.assertTemplateUsed(
            self.last_response, "post/detail.html"
        )
        self.assertTemplateUsed(
            self.last_response, "post/base.html"
        )
        self.assertTemplateUsed(
            self.last_response, "base.html"
        )

    def test_post_detail_404(self):
        """Do we return 404 for missing posts?"""
        self.get(
            "post_detail",
            year=2018,
            month=8,
            slug="nonexistent",
        )
        self.response_404()
