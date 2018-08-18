"""URL Paths and Routers for Organizer App"""
from django.urls import path

from .views import (
    NewsLinkAPIDetail,
    NewsLinkAPIList,
    StartupAPIDetail,
    StartupAPIList,
)
from .viewsets import TagViewSet

tag_create_list = TagViewSet.as_view(
    {"get": "list", "post": "create"}
)
tag_retrieve_update_delete = TagViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "delete",
    }
)

urlpatterns = [
    path("tag/", tag_create_list, name="api-tag-list"),
    path(
        "tag/<str:slug>/",
        tag_retrieve_update_delete,
        name="api-tag-detail",
    ),
    path(
        "startup/",
        StartupAPIList.as_view(),
        name="api-startup-list",
    ),
    path(
        "startup/<str:slug>/",
        StartupAPIDetail.as_view(),
        name="api-startup-detail",
    ),
    path(
        "newslink/",
        NewsLinkAPIList.as_view(),
        name="api-newslink-list",
    ),
    path(
        "newslink/<str:startup_slug>/<str:newslink_slug>/",
        NewsLinkAPIDetail.as_view(),
        name="api-newslink-detail",
    ),
]
