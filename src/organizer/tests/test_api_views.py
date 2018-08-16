"""Tests for Organizer Views"""
import json
from functools import partial

from test_plus import APITestCase

from config.test_utils import get_instance_data, omit_keys

from .factories import TagFactory

omit_id = partial(omit_keys, "id")
omit_url = partial(omit_keys, "url")


class TagAPITests(APITestCase):
    """Test API Views for Tag objects"""

    maxDiff = None

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of Tag objects"""
        tag_list = TagFactory.create_batch(10)
        self.get_check_200("api-tag-list")
        self.assertCountEqual(
            map(omit_url, self.response_json),
            [
                omit_id(get_instance_data(tag))
                for tag in tag_list
            ],
        )

    def test_list_404(self):
        """Do we generate a 404 if no tags?"""
        self.get("api-tag-list")
        self.response_404()

    def test_detail(self):
        """Is there a detail view for a Tag object"""
        tag = TagFactory()
        self.get_check_200("api-tag-detail", slug=tag.slug)
        self.assertEqual(
            omit_url(self.response_json),
            omit_id(get_instance_data(tag)),
        )

    def test_detail_404(self):
        """Do we generate 404 if tag not found?"""
        self.get("api-tag-detail", slug="nonexistent")
        self.response_404()
