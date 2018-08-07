"""Test the Admin functionality of the organizer App"""
from django.contrib.auth import get_user_model
from test_plus import TestCase

from config.test_utils import get_instance_data, omit_keys

from ..models import NewsLink, Startup, Tag
from .factories import (
    NewsLinkFactory,
    StartupFactory,
    TagFactory,
)


def get_startup_data(startup):
    """Strip unchecked fields from Startup"""
    return omit_keys(
        "id", "tags", get_instance_data(startup)
    )


def get_newslink_data(newslink):
    """Strip unchecked fields from NewsLink"""
    return omit_keys(
        "id", "startup", get_instance_data(newslink)
    )


class AdminSetupMixin:
    """Utility class to provide common setup pattern"""

    @classmethod
    def setUpTestData(cls):
        """Generate test data for entire suite"""
        User = get_user_model()
        cls.test_user = User.objects.create_superuser(
            username="testuser",
            email="admin@example.com",
            password="password",
        )


class TagAdminTests(AdminSetupMixin, TestCase):
    """Test suite for TagAdmin class"""

    @classmethod
    def setUpTestData(cls):
        """Generate test data for entire suite"""
        super().setUpTestData()
        cls.t1_pk = TagFactory().pk

    def test_list_get(self):
        """Is the admin list of Tags available?"""
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_tag_changelist"
            )

    def test_add_get(self):
        """Is the admin add form for Tags available?"""
        with self.login(self.test_user):
            self.get_check_200("admin:organizer_tag_add")

    def test_add_post(self):
        """Can new Tags be created?"""
        self.assertEqual(Tag.objects.count(), 1)
        data = get_instance_data(TagFactory.build())
        with self.login(self.test_user):
            self.post("admin:organizer_tag_add", data=data)
        self.assertEqual(Tag.objects.count(), 2)

    def test_change_get(self):
        """Is the admin Tag change-form available?"""
        # the Tag is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_tag_change",
                object_id=self.t1_pk,
            )

    def test_change_post(self):
        """Can existing Tags be modified?"""
        t2 = TagFactory()
        data = dict(name="a new tag name")
        self.assertNotEqual(get_instance_data(t2), data)
        with self.login(self.test_user):
            self.post(
                "admin:organizer_tag_change",
                data=data,
                object_id=t2.pk,
            )
            self.response_302()
        t2.refresh_from_db()
        self.assertEqual(
            omit_keys("id", "slug", get_instance_data(t2)),
            data,
        )
        self.assertEqual(Tag.objects.count(), 2)

    def test_delete_get(self):
        """Is the admin Tag delete-form available?"""
        # the Tag is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_tag_delete",
                object_id=self.t1_pk,
            )

    def test_delete_post(self):
        """Can Tags be deleted?"""
        # the Tag is created in setUpTestData
        t2_pk = TagFactory().pk
        with self.login(self.test_user):
            self.post(
                "admin:organizer_tag_delete",
                object_id=t2_pk,
                data=dict(post="yes"),
            )
            self.response_302()
        self.assertFalse(
            Tag.objects.filter(id=t2_pk).exists()
        )

    def test_history_get(self):
        """Is a Tag's history available?"""
        # the Tag is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_tag_history",
                object_id=self.t1_pk,
            )


class StartupAdminTests(AdminSetupMixin, TestCase):
    """Test suite for StartupAdmin class"""

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        """Generate test data for entire suite"""
        super().setUpTestData()
        cls.s1_pk = StartupFactory().pk
        cls.t1_pk = TagFactory().pk

    def test_list_get(self):
        """Is the admin list of Startups available?"""
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_startup_changelist"
            )

    def test_add_get(self):
        """Is the admin add form for Startups available?"""
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_startup_add"
            )

    def test_add_post(self):
        """Can new Startups be created?"""
        self.assertEqual(Startup.objects.count(), 1)
        startup_data = get_startup_data(
            StartupFactory.build()
        )
        # the tag below is created in setUpTestData
        data = dict(tags=[self.t1_pk], **startup_data)
        with self.login(self.test_user):
            self.post(
                "admin:organizer_startup_add", data=data
            )
        self.assertEqual(Startup.objects.count(), 2)

    def test_change_get(self):
        """Is the admin Startup change-form available?"""
        # the Startup is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_startup_change",
                object_id=self.s1_pk,
            )

    def test_change_post(self):
        """Can existing Startups be modified?"""
        s2 = StartupFactory()
        startup_data = get_startup_data(
            StartupFactory.build()
        )
        self.assertNotEqual(
            get_startup_data(s2), startup_data
        )
        # the tag below is created in setUpTestData
        data = dict(tags=[self.t1_pk], **startup_data)
        with self.login(self.test_user):
            self.post(
                "admin:organizer_startup_change",
                data=data,
                object_id=s2.pk,
            )
            self.response_302()
        s2.refresh_from_db()
        self.assertEqual(get_startup_data(s2), startup_data)
        self.assertEqual(Startup.objects.count(), 2)

    def test_delete_get(self):
        """Is the admin Startup delete-form available?"""
        # the Startup is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_startup_delete",
                object_id=self.s1_pk,
            )

    def test_delete_post(self):
        """Can Startups be deleted?"""
        # the Startup is created in setUpTestData
        s2_pk = StartupFactory().pk
        with self.login(self.test_user):
            self.post(
                "admin:organizer_startup_delete",
                object_id=s2_pk,
                data=dict(post="yes"),
            )
            self.response_302()
        self.assertFalse(
            Startup.objects.filter(id=s2_pk).exists()
        )

    def test_history_get(self):
        """Is a Startup's history available?"""
        # the Startup is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_startup_history",
                object_id=self.s1_pk,
            )


class NewsLinkAdminTests(AdminSetupMixin, TestCase):
    """Test suite for NewsLinkAdmin class"""

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        """Generate test data for entire suite"""
        super().setUpTestData()
        cls.nl1_pk = NewsLinkFactory().pk
        cls.s1_pk = StartupFactory().pk

    def test_list_get(self):
        """Is the admin list of NewsLinks available?"""
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_newslink_changelist"
            )

    def test_add_get(self):
        """Is the admin add form for NewsLinks available?"""
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_newslink_add"
            )

    def test_add_post(self):
        """Can new NewsLinks be created?"""
        self.assertEqual(NewsLink.objects.count(), 1)
        newslink_data = get_newslink_data(
            NewsLinkFactory.build()
        )
        # the startup below is created in setUpTestData
        data = dict(startup=self.s1_pk, **newslink_data)
        with self.login(self.test_user):
            self.post(
                "admin:organizer_newslink_add", data=data
            )
        self.assertEqual(NewsLink.objects.count(), 2)

    def test_change_get(self):
        """Is the admin NewsLink change-form available?"""
        # the NewsLink is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_newslink_change",
                object_id=self.nl1_pk,
            )

    def test_change_post(self):
        """Can existing NewsLinks be modified?"""
        nl2 = NewsLinkFactory()
        newslink_data = get_newslink_data(
            NewsLinkFactory.build()
        )
        self.assertNotEqual(
            get_newslink_data(nl2), newslink_data
        )
        # the startup below is created in setUpTestData
        data = dict(startup=self.s1_pk, **newslink_data)
        with self.login(self.test_user):
            self.post(
                "admin:organizer_newslink_change",
                data=data,
                object_id=nl2.pk,
            )
            self.response_302()
        nl2.refresh_from_db()
        self.assertEqual(
            get_newslink_data(nl2), newslink_data
        )
        self.assertEqual(nl2.startup.pk, self.s1_pk)
        self.assertEqual(NewsLink.objects.count(), 2)

    def test_delete_get(self):
        """Is the admin NewsLink delete-form available?"""
        # the NewsLink is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_newslink_delete",
                object_id=self.nl1_pk,
            )

    def test_delete_post(self):
        """Can NewsLinks be deleted?"""
        nl2_pk = NewsLinkFactory().pk
        with self.login(self.test_user):
            self.post(
                "admin:organizer_newslink_delete",
                object_id=nl2_pk,
                data=dict(post="yes"),
            )
            self.response_302()
        self.assertFalse(
            NewsLink.objects.filter(id=nl2_pk).exists()
        )

    def test_history_get(self):
        """Is a NewsLink's history available?"""
        # the NewsLink is created in setUpTestData
        with self.login(self.test_user):
            self.get_check_200(
                "admin:organizer_newslink_history",
                object_id=self.nl1_pk,
            )
