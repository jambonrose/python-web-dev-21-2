"""Viewsets for the Organizer App"""
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import ModelViewSet

from .models import NewsLink, Startup, Tag
from .serializers import (
    NewsLinkSerializer,
    StartupSerializer,
    TagSerializer,
)


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

    @action(detail=True, methods=["HEAD", "GET", "POST"])
    def tags(self, request, slug=None):
        """Relate a POSTed Tag to Startup in URI"""
        startup = self.get_object()
        if request.method in ("HEAD", "GET"):
            s_tag = TagSerializer(
                startup.tags,
                many=True,
                context={"request": request},
            )
            return Response(s_tag.data)
        tag_slug = request.data.get("slug")
        if not tag_slug:
            return Response(
                "Slug of Tag must be specified",
                status=HTTP_400_BAD_REQUEST,
            )
        tag = get_object_or_404(Tag, slug__iexact=tag_slug)
        startup.tags.add(tag)
        return Response(status=HTTP_204_NO_CONTENT)


class NewsLinkViewSet(ModelViewSet):
    """A set of views for the Startup model"""

    queryset = NewsLink.objects.all()
    serializer_class = NewsLinkSerializer

    def get_object(self):
        """Override DRF's generic method

        http://www.cdrf.co/3.7/rest_framework.viewsets/ModelViewSet.html#get_object
        """
        startup_slug = self.kwargs.get("startup_slug")
        newslink_slug = self.kwargs.get("newslink_slug")

        queryset = self.filter_queryset(self.get_queryset())

        newslink = get_object_or_404(
            queryset,
            slug=newslink_slug,
            startup__slug=startup_slug,
        )
        self.check_object_permissions(
            self.request, newslink
        )
        return newslink
