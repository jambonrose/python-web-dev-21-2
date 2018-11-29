"""URL paths for Blog App"""
from django.urls import path

from .views import (
    PostCreate,
    PostDelete,
    PostDetail,
    PostList,
    PostUpdate,
)

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path(
        "create/", PostCreate.as_view(), name="post_create"
    ),
    path(
        "<int:year>/<int:month>/<str:slug>/",
        PostDetail.as_view(),
        name="post_detail",
    ),
    path(
        "<int:year>/<int:month>/<str:slug>/delete/",
        PostDelete.as_view(),
        name="post_delete",
    ),
    path(
        "<int:year>/<int:month>/<str:slug>/update/",
        PostUpdate.as_view(),
        name="post_update",
    ),
]
