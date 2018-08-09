"""Views for Organizer App"""
from django.http import JsonResponse
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
)
from django.views import View

from .models import Tag
from .serializers import TagSerializer


class TagAPIDetail(View):
    """Return JSON for single Tag object"""

    def get(self, request, pk):
        """Handle GET HTTP method"""
        tag = get_object_or_404(Tag, pk=pk)
        s_tag = TagSerializer(tag)
        return JsonResponse(s_tag.data)


class TagAPIList(View):
    """Return JSON for multiple Tag objects"""

    def get(self, request):
        """Handle GET HTTP method"""
        tag_list = get_list_or_404(Tag)
        s_tag = TagSerializer(tag_list, many=True)
        return JsonResponse(s_tag.data, safe=False)
