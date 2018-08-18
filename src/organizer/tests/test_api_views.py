"""Tests for Organizer Views"""
import json

from test_plus import APITestCase

from config.test_utils import context_kwarg, reverse

from ..models import Tag
from ..serializers import (
    NewsLinkSerializer,
    StartupSerializer,
    TagSerializer,
)
from .factories import (
    NewsLinkFactory,
    StartupFactory,
    TagFactory,
)


class TagAPITests(APITestCase):
    """Test API Views for Tag objects"""

    maxDiff = None

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of Tag objects"""
        url_name = "api-tag-list"
        tag_list = TagFactory.create_batch(10)
        self.get_check_200(url_name)
        self.assertCountEqual(
            self.response_json,
            TagSerializer(
                tag_list,
                many=True,
                **context_kwarg(reverse(url_name))
            ).data,
        )

    def test_list_empty(self):
        """Do we return an empty list if no tags?"""
        self.get_check_200("api-tag-list")
        self.assertEquals(self.response_json, [])

    def test_list_create(self):
        """Does Tag list view create new objects via POST?"""
        self.assertEqual(Tag.objects.count(), 0)
        self.post("api-tag-list", data={"name": "django"})
        self.response_201()
        self.assertEqual(Tag.objects.count(), 1)

    def test_detail(self):
        """Is there a detail view for a Tag object"""
        tag = TagFactory()
        url = reverse("api-tag-detail", slug=tag.slug)
        self.get_check_200(url)
        self.assertCountEqual(
            self.response_json,
            TagSerializer(tag, **context_kwarg(url)).data,
        )

    def test_detail_404(self):
        """Do we generate 404 if tag not found?"""
        self.get("api-tag-detail", slug="nonexistent")
        self.response_404()

    def test_detail_update(self):
        """Can we update a Tag via PUT?"""
        tag = TagFactory(name="first")
        url = reverse("api-tag-detail", slug=tag.slug)
        self.put(url, data={"name": "second"})
        self.response_200()
        tag.refresh_from_db()
        self.assertEqual(tag.name, "second")

    def test_detail_update_404(self):
        """Do we generate 404 if tag not found?"""
        url = reverse("api-tag-detail", slug="nonexistent")
        self.put(url, data={"name": "second"})
        self.response_404()

    def test_detail_partial_update(self):
        """Can we update a Tag via PATCH?"""
        tag = TagFactory(name="first")
        url = reverse("api-tag-detail", slug=tag.slug)
        self.patch(url, data={"name": "second"})
        self.response_200()
        tag.refresh_from_db()
        self.assertEqual(tag.name, "second")

    def test_detail_partial_update_404(self):
        """Do we generate 404 if tag not found?"""
        url = reverse("api-tag-detail", slug="nonexistent")
        self.patch(url, data={"name": "second"})
        self.response_404()

    def test_detail_delete(self):
        """Can we delete a tag?"""
        tag = TagFactory()
        self.delete("api-tag-detail", slug=tag.slug)
        self.response_204()
        self.assertFalse(
            Tag.objects.filter(pk=tag.pk).exists()
        )

    def test_detail_delete_404(self):
        """Do we generate 404 if tag not found?"""
        self.delete("api-tag-detail", slug="nonexistent")
        self.response_404()


class StartupAPITests(APITestCase):
    """Test API Views for Startup objects"""

    maxDiff = None

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of Startup objects"""
        url_name = "api-startup-list"
        startup_list = StartupFactory.create_batch(10)
        self.get_check_200(url_name)
        self.assertCountEqual(
            self.response_json,
            StartupSerializer(
                startup_list,
                many=True,
                **context_kwarg(reverse(url_name))
            ).data,
        )

    def test_list_empty(self):
        """Do we return an empty list if no startups?"""
        self.get_check_200("api-startup-list")
        self.assertEquals(self.response_json, [])

    def test_detail(self):
        """Is there a detail view for a Startup object"""
        startup = StartupFactory()
        url = reverse(
            "api-startup-detail", slug=startup.slug
        )
        self.get_check_200(url)
        self.assertCountEqual(
            self.response_json,
            StartupSerializer(
                startup, **context_kwarg(url)
            ).data,
        )

    def test_detail_404(self):
        """Do we generate 404 if startup not found?"""
        self.get("api-startup-detail", pk=1)
        self.response_404()


class NewsLinkAPITests(APITestCase):
    """Test API Views for NewsLink objects"""

    maxDiff = None

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of NewsLink objects"""
        url_name = "api-newslink-list"
        newslink_list = NewsLinkFactory.create_batch(10)
        self.get_check_200(url_name)
        self.assertCountEqual(
            self.response_json,
            NewsLinkSerializer(
                newslink_list,
                many=True,
                **context_kwarg(reverse(url_name))
            ).data,
        )

    def test_list_empty(self):
        """Do we return an empty list if no articles?"""
        self.get_check_200("api-newslink-list")
        self.assertEquals(self.response_json, [])

    def test_detail(self):
        """Is there a detail view for a NewsLink object"""
        newslink = NewsLinkFactory()
        url = reverse(
            "api-newslink-detail",
            startup_slug=newslink.startup.slug,
            newslink_slug=newslink.slug,
        )
        self.get_check_200(url)
        self.assertCountEqual(
            self.response_json,
            NewsLinkSerializer(
                newslink, **context_kwarg(url)
            ).data,
        )

    def test_detail_404(self):
        """Do we generate 404 if newslink not found?"""
        self.get(
            "api-newslink-detail",
            startup_slug="django",
            newslink_slug="the-best",
        )
        self.response_404()
