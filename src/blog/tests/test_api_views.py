"""Tests for Blog Views"""
import json

from test_plus import APITestCase

from config.test_utils import context_kwarg, reverse

from ..serializers import PostSerializer
from .factories import PostFactory


class PostAPITests(APITestCase):
    """Test API views for Post objects"""

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of Post objects"""
        url_name = "api-post-list"
        post_list = PostFactory.create_batch(10)
        self.get_check_200(url_name)
        self.assertCountEqual(
            self.response_json,
            PostSerializer(
                post_list,
                many=True,
                **context_kwarg(reverse(url_name))
            ).data,
        )

    def test_list_404(self):
        """Do we return an empty list if no posts?"""
        self.get_check_200("api-post-list")

    def test_detail(self):
        """Is there a detail view for a Post object"""
        post = PostFactory()
        url = reverse(
            "api-post-detail",
            year=post.pub_date.year,
            month=post.pub_date.month,
            slug=post.slug,
        )
        self.get_check_200(url)
        self.assertCountEqual(
            self.response_json,
            PostSerializer(post, **context_kwarg(url)).data,
        )

    def test_detail_404(self):
        """Do we generate 404 if post not found?"""
        self.get(
            "api-post-detail",
            year=2018,
            month=8,
            slug="now-recording",
        )
        self.response_404()
