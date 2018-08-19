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

    def create(self, validated_data):
        """Create Startup and associate Tags"""
        tag_data_list = validated_data.pop("tags")
        startup = Startup.objects.create(**validated_data)
        # the code below, where we relate bulk-creates objects,
        # works only in databases that returns PK after bulk insert,
        # which at the time of writing is only PostgreSQL
        tag_list = Tag.objects.bulk_create(
            [Tag(**tag_data) for tag_data in tag_data_list]
        )
        startup.tags.add(*tag_list)
        return startup


class NewsLinkSerializer(ModelSerializer):
    """Serialize NewsLink data"""

    startup = StartupSerializer()

    class Meta:
        model = NewsLink
        fields = "__all__"
