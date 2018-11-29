"""Views for Organizer App"""
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import NewsLink, Startup, Tag
from .serializers import NewsLinkSerializer


class TagList(ListView):
    """Display a list of Tags"""

    queryset = Tag.objects.all()
    template_name = "tag/list.html"


class TagDetail(DetailView):
    """Display a single Tag"""

    queryset = Tag.objects.all()
    template_name = "tag/detail.html"


class StartupList(ListView):
    """Display a list of Startups"""

    queryset = Startup.objects.all()
    template_name = "startup/list.html"


class StartupDetail(DetailView):
    """Display a single Startup"""

    queryset = Startup.objects.all()
    template_name = "startup/detail.html"


class NewsLinkAPIDetail(RetrieveUpdateDestroyAPIView):
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


class NewsLinkAPIList(ListCreateAPIView):
    """Return JSON for multiple NewsLink objects"""

    queryset = NewsLink.objects.all()
    serializer_class = NewsLinkSerializer
