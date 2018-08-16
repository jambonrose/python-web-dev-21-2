"""Views for Organizer App"""
import json

from django.http import Http404, HttpResponse
from django.views import View

from .models import Tag


class TagAPIDetail(View):
    """Return JSON for single Tag object"""

    def get(self, request, pk):
        """Handle GET HTTP method"""
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")
        tag_json = json.dumps(
            dict(id=tag.pk, name=tag.name, slug=tag.slug)
        )
        return HttpResponse(tag_json)


class TagAPIList(View):
    """Return JSON for multiple Tag objects"""

    def get(self, request):
        """Handle GET HTTP method"""
        tag_list = Tag.objects.all()
        if not tag_list:
            raise Http404("No tags found")
        tag_json = json.dumps(
            [
                dict(
                    id=tag.pk, name=tag.name, slug=tag.slug
                )
                for tag in tag_list
            ]
        )
        return HttpResponse(tag_json)
