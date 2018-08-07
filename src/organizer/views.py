"""Views for Organizer App"""
import json

from django.http import HttpResponse
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
)
from django.views import View

from .models import Tag


def serialize_tag_to_dict(tag):
    """Tag -> Python Dict"""
    return dict(id=tag.pk, name=tag.name, slug=tag.slug)


def serialize_tag_to_json(tag):
    """Tag -> JSON"""
    return json.dumps(serialize_tag_to_dict(tag))


def serialize_tag_list_to_json(tag_list):
    """[Tag] -> JSON"""
    return json.dumps(
        [serialize_tag_to_dict(tag) for tag in tag_list]
    )


class TagAPIDetail(View):
    """Return JSON for single Tag object"""

    def get(self, request, pk):
        """Handle GET HTTP method"""
        tag = get_object_or_404(Tag, pk=pk)
        tag_json = serialize_tag_to_json(tag)
        return HttpResponse(
            tag_json, content_type="application/json"
        )


class TagAPIList(View):
    """Return JSON for multiple Tag objects"""

    def get(self, request):
        """Handle GET HTTP method"""
        tag_list = get_list_or_404(Tag)
        tag_json = serialize_tag_list_to_json(tag_list)
        return HttpResponse(
            tag_json, content_type="application/json"
        )
