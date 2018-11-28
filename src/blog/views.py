"""Views for Blog App"""
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
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


class PostAPIList(ListAPIView):
    """Return data for multiple Post objects"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request):
        """Create new Post upon POST"""
        s_post = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if s_post.is_valid():
            s_post.save()
            return Response(
                s_post.data, status=HTTP_201_CREATED
            )
        return Response(
            s_post.errors, status=HTTP_400_BAD_REQUEST
        )


class PostAPIDetail(RetrieveAPIView):
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

    def put(self, request, *args, **kwargs):
        """Update Post object with new data from PUT

        Type signature could also be:
            def put(self, request, year, month, slug)

        Given that we don't use any of the key-word
        arguments, we simplify the signature with Python's
        args/kwargs signature.
        """
        post = self.get_object()
        s_post = self.serializer_class(
            post,
            data=request.data,
            context={"request": request},
        )
        if s_post.is_valid():
            s_post.save()
            return Response(s_post.data, status=HTTP_200_OK)
        return Response(
            s_post.errors, status=HTTP_400_BAD_REQUEST
        )

    def patch(self, request, *args, **kwargs):
        """Update Post object with new data from PATCH

        Type signature could also be:
            def patch(self, request, year, month, slug)

        Given that we don't use any of the key-word
        arguments, we simplify the signature with Python's
        args/kwargs signature.
        """
        post = self.get_object()
        s_post = self.serializer_class(
            post,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if s_post.is_valid():
            s_post.save()
            return Response(s_post.data, status=HTTP_200_OK)
        return Response(
            s_post.errors, status=HTTP_400_BAD_REQUEST
        )
