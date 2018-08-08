"""Serializers for the Organizer App

Serializer Documentation
http://www.django-rest-framework.org/api-guide/serializers/
http://www.django-rest-framework.org/api-guide/fields/
http://www.django-rest-framework.org/api-guide/relations/
"""
from rest_framework.fields import (
    CharField,
    DateField,
    EmailField,
    IntegerField,
    SlugField,
    URLField,
)
from rest_framework.serializers import Serializer


class TagSerializer(Serializer):
    """Serialize Tag data"""

    id = IntegerField(read_only=True)
    name = CharField(max_length=31)
    slug = SlugField(max_length=31, allow_blank=True)


class StartupSerializer(Serializer):
    """Serialize Startup data"""

    id = IntegerField(read_only=True)
    name = CharField(max_length=31)
    slug = SlugField(max_length=31)
    description = CharField()
    founded_date = DateField()
    contact = EmailField()
    website = URLField(
        max_length=255  # https://tools.ietf.org/html/rfc3986
    )
    tags = TagSerializer(many=True)


class NewsLinkSerializer(Serializer):
    """Serialize NewsLink data"""

    id = IntegerField(read_only=True)
    title = CharField(max_length=63)
    slug = SlugField(max_length=63)
    pub_date = DateField()
    link = URLField(
        max_length=255  # https://tools.ietf.org/html/rfc3986
    )
    startup = StartupSerializer()
