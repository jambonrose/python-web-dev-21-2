"""Test the Admin functionality of the blog App"""
from django.contrib.auth import get_user_model
from test_plus import TestCase

from config.test_utils import get_instance_data, omit_keys
from organizer.tests.factories import (
    StartupFactory,
    TagFactory,
)

from ..models import Post
from .factories import PostFactory


def get_post_data(post):
    """Strip post of unchecked fields"""
    return omit_keys(
        "id", "tags", "startups", get_instance_data(post)
    )


class AdminTests(TestCase):
    """Test Suite for PostAdmin"""

    @classmethod
    def setUpTestData(cls):
        """Generate test data for entire suite"""
        User = get_user_model()
        cls.test_user = User.objects.create_superuser(
            username="testuser",
            email="admin@example.com",
            password="password",
        )
        cls.p1_pk = PostFactory().pk
        cls.t1_pk = TagFactory().pk
        cls.s1_pk = StartupFactory().pk

    def test_post_list_get(self):
        """Is the admin list of Posts available?"""
        with self.login(self.test_user):
            self.get_check_200("admin:blog_post_changelist")

    def test_post_add_get(self):
        """Is the admin add form for Posts available?"""
        with self.login(self.test_user):
            self.get_check_200("admin:blog_post_add")

    def test_post_add_post(self):
        """Can new Posts be created?"""
        self.assertEqual(Post.objects.count(), 1)
        post_data = get_post_data(PostFactory.build())
        # the tag and startup below are created in setUpTestData
        data = dict(
            tags=[self.t1_pk],
            startups=[self.s1_pk],
            **post_data
        )
        with self.login(self.test_user):
            self.post("admin:blog_post_add", data=data)
        self.assertEqual(Post.objects.count(), 2)

    def test_post_change_get(self):
        """Is the admin Post change-form available?"""
        # the Post is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:blog_post_change",
                object_id=self.p1_pk,
            )

    def test_post_change_post(self):
        """Can existing Posts be modified?"""
        p2 = PostFactory()
        post_data = get_post_data(PostFactory.build())
        self.assertNotEqual(get_post_data(p2), post_data)
        # the tag and startup below are created in setUpTestData
        data = dict(
            tags=[self.t1_pk],
            startups=[self.s1_pk],
            **post_data
        )
        with self.login(self.test_user):
            self.post(
                "admin:blog_post_change",
                data=data,
                object_id=p2.pk,
            )
            self.response_302()
        p2.refresh_from_db()
        self.assertEqual(get_post_data(p2), post_data)
        self.assertEqual(Post.objects.count(), 2)

    def test_post_delete_get(self):
        """Is the admin Post delete-form available?"""
        # the Post is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:blog_post_delete",
                object_id=self.p1_pk,
            )

    def test_post_delete_post(self):
        """Can Posts be deleted?"""
        # the Post is created in setUpTestData
        p2_pk = PostFactory().pk
        with self.login(self.test_user):
            self.post(
                "admin:blog_post_delete",
                object_id=p2_pk,
                data=dict(post="yes"),
            )
            self.response_302()
        self.assertFalse(
            Post.objects.filter(id=p2_pk).exists()
        )

    def test_post_history_get(self):
        """Is a Post's history available?"""
        # the Post is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:blog_post_history",
                object_id=self.p1_pk,
            )
