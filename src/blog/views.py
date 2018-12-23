"""Views for Blog App"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Post


class PostObjectMixin:
    """Django View mix-in to find blog posts"""

    model = Post

    def get_object(self, queryset=None):
        """Get a blog post using year, month, and slug

        http://ccbv.co.uk/SingleObjectMixin
        """
        if queryset is None:
            queryset = self.get_queryset()

        year, month, slug = map(
            self.kwargs.get, ["year", "month", "slug"]
        )
        if any(arg is None for arg in (year, month, slug)):
            raise AttributeError(
                f"View {self.__class__.__name__} must be"
                f"called with year, month, and slug for"
                f"Post objects"
            )
        return get_object_or_404(
            queryset,
            pub_date__year=year,
            pub_date__month=month,
            slug=slug,
        )


class PostCreate(LoginRequiredMixin, CreateView):
    """Create new blog posts"""

    form_class = PostForm
    model = Post
    template_name = "post/form.html"
    extra_context = {"update": False}


class PostDetail(PostObjectMixin, DetailView):
    """Display a single blog Post"""

    template_name = "post/detail.html"


class PostDelete(
    PostObjectMixin, LoginRequiredMixin, DeleteView
):
    """Delete a single blog post"""

    template_name = "post/confirm_delete.html"
    success_url = reverse_lazy("post_list")


class PostList(ListView):
    """Display a list of blog Posts"""

    model = Post
    template_name = "post/list.html"


class PostUpdate(
    PostObjectMixin, LoginRequiredMixin, UpdateView
):
    """Update existing blog posts"""

    form_class = PostForm
    template_name = "post/form.html"
    extra_context = {"update": True}
