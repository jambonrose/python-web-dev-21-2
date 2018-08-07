"""Tests for Organizer Views"""
import json

from test_plus import APITestCase

from config.test_utils import get_instance_data

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
        tag_list = TagFactory.create_batch(10)
        self.get_check_200("api-tag-list")
        self.assertCountEqual(
            self.response_json,
            map(get_instance_data, tag_list),
        )

    def test_detail(self):
        """Is there a detail view for a Tag object"""
        tag = TagFactory()
        self.get_check_200("api-tag-detail", pk=tag.pk)
        self.assertEqual(
            self.response_json, get_instance_data(tag)
        )
