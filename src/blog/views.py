"""Views for Blog App"""
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from .models import Post


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
