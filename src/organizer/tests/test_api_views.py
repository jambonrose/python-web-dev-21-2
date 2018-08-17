"""Tests for Organizer Views"""
import json

from test_plus import APITestCase

from config.test_utils import context_kwarg, reverse

from ..serializers import TagSerializer
from .factories import TagFactory


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

    def test_list_404(self):
        """Do we generate a 404 if no tags?"""
        self.get("api-tag-list")
        self.response_404()

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
