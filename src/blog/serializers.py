"""Serializers for th Blog App

Serializer Documentation
http://www.django-rest-framework.org/api-guide/serializers/
http://www.django-rest-framework.org/api-guide/fields/
http://www.django-rest-framework.org/api-guide/relations/
"""

from rest_framework.reverse import reverse
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from organizer.serializers import (
    StartupSerializer,
    TagSerializer,
)

from .models import Post


class PostSerializer(ModelSerializer):
    """Serialize Post data"""

    url = SerializerMethodField()
    tags = TagSerializer(many=True)
    startups = StartupSerializer(many=True)

    class Meta:
        model = Post
        exclude = ("id",)

    def get_url(self, post):
        """Return full API URL for serialized POST object"""
        return reverse(
            "api-post-detail",
            kwargs=dict(
                year=post.pub_date.year,
                month=post.pub_date.month,
                slug=post.slug,
            ),
            request=self.context["request"],
        )
