"""Serializers for th Blog App

Serializer Documentation
http://www.django-rest-framework.org/api-guide/serializers/
http://www.django-rest-framework.org/api-guide/fields/
http://www.django-rest-framework.org/api-guide/relations/
"""

from rest_framework.reverse import reverse
from rest_framework.serializers import (
    HyperlinkedRelatedField,
    ModelSerializer,
    SerializerMethodField,
)

from organizer.models import Startup, Tag

from .models import Post


class PostSerializer(ModelSerializer):
    """Serialize Post data"""

    url = SerializerMethodField()
    tags = HyperlinkedRelatedField(
        lookup_field="slug",
        many=True,
        queryset=Tag.objects.all(),
        view_name="api-tag-detail",
    )
    startups = HyperlinkedRelatedField(
        lookup_field="slug",
        many=True,
        queryset=Startup.objects.all(),
        view_name="api-startup-detail",
    )

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
