"""URL paths for Blog App"""
from django.urls import path

from .views import PostDetail, PostList

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<str:slug>/",
        PostDetail.as_view(),
        name="post_detail",
    ),
]
