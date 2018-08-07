"""Views for Organizer App"""
import json

from django.http import HttpResponse
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
)
from django.views import View

from .models import Tag


class TagAPIDetail(View):
    """Return JSON for single Tag object"""

    def get(self, request, pk):
        """Handle GET HTTP method"""
        tag = get_object_or_404(Tag, pk=pk)
        tag_json = json.dumps(
            dict(id=tag.pk, name=tag.name, slug=tag.slug)
        )
        return HttpResponse(tag_json)


class TagAPIList(View):
    """Return JSON for multiple Tag objects"""

    def get(self, request):
        """Handle GET HTTP method"""
        tag_list = get_list_or_404(Tag)
        tag_json = json.dumps(
            [
                dict(
                    id=tag.pk, name=tag.name, slug=tag.slug
                )
                for tag in tag_list
            ]
        )
        return HttpResponse(tag_json)
