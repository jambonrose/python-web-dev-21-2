"""Views for Blog App"""
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Post
from .serializers import PostSerializer


class PostList(ListView):
    """Display a list of blog Posts"""

    model = Post
    template_name = "post/list.html"


class PostDetail(View):
    """Display a single blog Post"""

    def get(self, request, year, month, slug):
        """Handle GET request of Post detail"""
        post = get_object_or_404(
            Post,
            pub_date__year=year,
            pub_date__month=month,
            slug=slug,
        )
        return render(
            request, "post/detail.html", {"post": post}
        )


class PostAPIList(ListCreateAPIView):
    """Return data for multiple Post objects"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostAPIDetail(RetrieveUpdateDestroyAPIView):
    """Return data for a single Post object"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self):
        """Override DRF's generic method

        http://www.cdrf.co/3.7/rest_framework.generics/ListAPIView.html#get_object
        """
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        slug = self.kwargs.get("slug")

        queryset = self.filter_queryset(self.get_queryset())

        post = get_object_or_404(
            queryset,
            pub_date__year=year,
            pub_date__month=month,
            slug=slug,
        )
        self.check_object_permissions(self.request, post)
        return post
