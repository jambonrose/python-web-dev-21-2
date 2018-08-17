"""Views for Organizer App"""
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Startup, Tag
from .serializers import StartupSerializer, TagSerializer


class TagAPIDetail(APIView):
    """Return JSON for single Tag object"""

    def get(self, request, slug):
        """Handle GET HTTP method"""
        tag = get_object_or_404(Tag, slug=slug)
        s_tag = TagSerializer(
            tag, context={"request": request}
        )
        return Response(s_tag.data)


class TagAPIList(APIView):
    """Return JSON for multiple Tag objects"""

    def get(self, request):
        """Handle GET HTTP method"""
        tag_list = get_list_or_404(Tag)
        s_tag = TagSerializer(
            tag_list,
            many=True,
            context={"request": request},
        )
        return Response(s_tag.data)


class StartupAPIDetail(APIView):
    """Return JSON for single Startup object"""

    def get(self, request, slug):
        """Handle GET HTTP method"""
        startup = get_object_or_404(Startup, slug=slug)
        s_startup = StartupSerializer(
            startup, context={"request": request}
        )
        return Response(s_startup.data)


class StartupAPIList(APIView):
    """Return JSON for multiple Startup objects"""

    def get(self, request):
        """Handle GET HTTP method"""
        startup_list = get_list_or_404(Startup)
        s_startup = StartupSerializer(
            startup_list,
            many=True,
            context={"request": request},
        )
        return Response(s_startup.data)
