"""Serializers for the Organizer App

Serializer Documentation
http://www.django-rest-framework.org/api-guide/serializers/
http://www.django-rest-framework.org/api-guide/fields/
"""
from rest_framework.fields import (
    CharField,
    IntegerField,
    SlugField,
)
from rest_framework.serializers import Serializer


class TagSerializer(Serializer):
    """Serialize Tag data"""

    id = IntegerField(read_only=True)
    name = CharField(max_length=31)
    slug = SlugField(max_length=31, allow_blank=True)
