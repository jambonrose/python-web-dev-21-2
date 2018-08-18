"""Viewsets for the Organizer App"""
from rest_framework.viewsets import ModelViewSet

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ModelViewSet):
    """A set of views for the Tag model"""

    lookup_field = "slug"
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
