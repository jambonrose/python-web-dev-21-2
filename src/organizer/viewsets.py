"""Viewsets for the Organizer App"""
from rest_framework.viewsets import ModelViewSet

from .models import Startup, Tag
from .serializers import StartupSerializer, TagSerializer


class TagViewSet(ModelViewSet):
    """A set of views for the Tag model"""

    lookup_field = "slug"
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class StartupViewSet(ModelViewSet):
    """A set of views for the Startup model"""

    lookup_field = "slug"
    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
