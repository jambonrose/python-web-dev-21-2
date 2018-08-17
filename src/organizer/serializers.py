"""Serializers for the Organizer App

Serializer Documentation
http://www.django-rest-framework.org/api-guide/serializers/
http://www.django-rest-framework.org/api-guide/fields/
http://www.django-rest-framework.org/api-guide/relations/
"""
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from .models import NewsLink, Startup, Tag


class TagSerializer(HyperlinkedModelSerializer):
    """Serialize Tag data"""

    class Meta:
        model = Tag
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
                "view_name": "api-tag-detail",
            }
        }


class StartupSerializer(HyperlinkedModelSerializer):
    """Serialize Startup data"""

    tags = TagSerializer(many=True)

    class Meta:
        model = Startup
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug",
                "view_name": "api-startup-detail",
            }
        }


class NewsLinkSerializer(ModelSerializer):
    """Serialize NewsLink data"""

    startup = StartupSerializer()

    class Meta:
        model = NewsLink
        fields = "__all__"
