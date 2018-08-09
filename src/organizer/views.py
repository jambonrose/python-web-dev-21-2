"""Views for Organizer App"""
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagSerializer


class TagAPIDetail(APIView):
    """Return JSON for single Tag object"""

    def get(self, request, pk):
        """Handle GET HTTP method"""
        tag = get_object_or_404(Tag, pk=pk)
        s_tag = TagSerializer(tag)
        return Response(s_tag.data)


class TagAPIList(APIView):
    """Return JSON for multiple Tag objects"""

    def get(self, request):
        """Handle GET HTTP method"""
        tag_list = get_list_or_404(Tag)
        s_tag = TagSerializer(tag_list, many=True)
        return Response(s_tag.data)
