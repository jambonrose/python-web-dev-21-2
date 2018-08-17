"""Views for Organizer App"""
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.views.decorators.http import require_safe
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

from .models import NewsLink, Startup, Tag
from .serializers import (
    NewsLinkSerializer,
    StartupSerializer,
    TagSerializer,
)


@require_safe
def tag_list(request):
    """Render an HTML template of a list of tags"""
    tag_list = Tag.objects.all()
    template = loader.get_template("tag/list.html")
    context = {"tag_list": tag_list}
    html_content = template.render(context)
    return HttpResponse(html_content)


@require_safe
def tag_detail(request, slug):
    """Render an HTML template of a tags"""
    tag = get_object_or_404(Tag, slug=slug)
    template = loader.get_template("tag/detail.html")
    context = {"tag": tag}
    html_content = template.render(context)
    return HttpResponse(html_content)


class TagAPIDetail(RetrieveAPIView):
    """Return JSON for single Tag object"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"


class TagAPIList(ListAPIView):
    """Return JSON for multiple Tag objects"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class StartupAPIDetail(RetrieveAPIView):
    """Return JSON for single Startup object"""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    lookup_field = "slug"


class StartupAPIList(ListAPIView):
    """Return JSON for multiple Startup objects"""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer


class NewsLinkAPIDetail(RetrieveAPIView):
    """Return JSON for single NewsLink object"""

    queryset = NewsLink.objects.all()
    serializer_class = NewsLinkSerializer

    def get_object(self):
        """Override DRF's generic method

        http://www.cdrf.co/3.7/rest_framework.generics/ListAPIView.html#get_object
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


class NewsLinkAPIList(ListAPIView):
    """Return JSON for multiple NewsLink objects"""

    queryset = NewsLink.objects.all()
    serializer_class = NewsLinkSerializer
