"""Viewsets for the Organizer App"""
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import ViewSet

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ViewSet):
    """A set of views for the Tag model"""

    def list(self, request):
        """List Tag objects"""
        tag_list = Tag.objects.all()
        s_tag = TagSerializer(
            tag_list,
            many=True,
            context={"request": request},
        )
        return Response(s_tag.data)

    def retrieve(self, request, slug):
        """Display a single Tag object"""
        tag = get_object_or_404(Tag, slug=slug)
        s_tag = TagSerializer(
            tag, context={"request": request}
        )
        return Response(s_tag.data)

    def create(self, request):
        """Create a new Tag object"""
        s_tag = TagSerializer(
            data=request.data, context={"request": request}
        )
        if s_tag.is_valid():
            s_tag.save()
        return Response(s_tag.data, status=HTTP_201_CREATED)

    def update(self, request, slug):
        """Update an existing Tag object"""
        tag = get_object_or_404(Tag, slug=slug)
        s_tag = TagSerializer(
            tag,
            data=request.data,
            context={"request": request},
        )
        if s_tag.is_valid():
            s_tag.save()
            return Response(s_tag.data)
        return Response(
            s_tag.errors, status=HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, slug):
        """Update a Tag object partially"""
        tag = get_object_or_404(Tag, slug=slug)
        s_tag = TagSerializer(
            tag,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if s_tag.is_valid():
            s_tag.save()
            return Response(s_tag.data)
        return Response(
            s_tag.errors, status=HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug):
        """Delete a Tag object"""
        tag = get_object_or_404(Tag, slug=slug)
        tag.delete()
        return Response(status=HTTP_204_NO_CONTENT)
