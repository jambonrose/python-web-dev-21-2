"""Tests for (traditional/HTML) views for Organizer App"""
from random import randint

from test_plus import TestCase

from config.test_utils import (
    get_instance_data,
    omit_keys,
    reverse,
)
from organizer.tests.factories import (
    StartupFactory,
    TagFactory,
)

from ..forms import PostForm
from ..models import Post
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

    def test_create_get(self):
        """Can we view the form to create Posts?"""
        response = self.get_check_200("post_create")
        form = self.get_context("form")
        self.assertIsInstance(form, PostForm)
        self.assertContext("update", False)
        self.assertTemplateUsed(response, "post/form.html")
        self.assertTemplateUsed(response, "post/base.html")
        self.assertTemplateUsed(response, "base.html")

    def test_create_post(self):
        """Can we submit a form to create Posts?"""
        post_num = Post.objects.count()
        tag = TagFactory()
        startup = StartupFactory()
        post_data = {
            **omit_keys(
                "id", get_instance_data(PostFactory.build())
            ),
            "tags": [tag.pk],
            "startups": [startup.pk],
        }
        self.assertFalse(
            Post.objects.filter(
                slug=post_data["slug"]
            ).exists()
        )
        response = self.post("post_create", data=post_data)
        self.assertEqual(
            Post.objects.count(),
            post_num + 1,
            response.content.decode("utf8"),
        )
        post = Post.objects.get(slug=post_data["slug"])
        self.assertIn(tag, post.tags.all())
        self.assertIn(startup, post.startups.all())
        self.assertRedirects(
            response, post.get_absolute_url()
        )

    def test_update_get(self):
        """Can we view a form to update posts?"""
        post = PostFactory()
        response = self.get_check_200(
            "post_update",
            year=post.pub_date.year,
            month=post.pub_date.month,
            slug=post.slug,
        )
        form = self.get_context("form")
        self.assertIsInstance(form, PostForm)
        context_post = self.get_context("post")
        self.assertEqual(post.pk, context_post.pk)
        self.assertContext("update", True)
        self.assertTemplateUsed(response, "post/form.html")
        self.assertTemplateUsed(response, "post/base.html")
        self.assertTemplateUsed(response, "base.html")

    def test_update_post(self):
        """Can we submit a form to update posts?"""
        post = PostFactory(
            tags=TagFactory.create_batch(randint(1, 5)),
            startups=StartupFactory.create_batch(
                randint(1, 5)
            ),
        )
        self.assertNotEqual(post.title, "django")
        post_data = omit_keys("id", get_instance_data(post))
        response = self.post(
            "post_update",
            year=post.pub_date.year,
            month=post.pub_date.month,
            slug=post.slug,
            data=dict(post_data, title="django"),
        )
        post.refresh_from_db()
        self.assertEqual(
            post.title,
            "django",
            response.content.decode("utf8"),
        )
        self.assertRedirects(
            response, post.get_absolute_url()
        )

    def test_delete_get(self):
        """Can we view a form to delete a Post?"""
        post = PostFactory()
        response = self.get_check_200(
            "post_delete",
            year=post.pub_date.year,
            month=post.pub_date.month,
            slug=post.slug,
        )
        context_post = self.get_context("post")
        self.assertEqual(post.pk, context_post.pk)
        self.assertTemplateUsed(
            response, "post/confirm_delete.html"
        )
        self.assertTemplateUsed(response, "post/base.html")
        self.assertTemplateUsed(response, "base.html")

    def test_delete_post(self):
        """Can we submit a form to delete a Post?"""
        post = PostFactory()
        response = self.post(
            "post_delete",
            year=post.pub_date.year,
            month=post.pub_date.month,
            slug=post.slug,
        )
        self.assertRedirects(response, reverse("post_list"))
        self.assertFalse(
            Post.objects.filter(pk=post.pk).exists()
        )
