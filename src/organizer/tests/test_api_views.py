"""Tests for Organizer Views"""
import json

from test_plus import APITestCase

from config.test_utils import context_kwarg, reverse

from ..serializers import StartupSerializer, TagSerializer
from .factories import StartupFactory, TagFactory


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
