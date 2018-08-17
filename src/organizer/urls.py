"""URL Configuration for Organizer App"""
from django.urls import path

from .views import (
    NewsLinkAPIDetail,
    NewsLinkAPIList,
    StartupAPIDetail,
    StartupAPIList,
    TagAPIDetail,
    TagAPIList,
)

urlpatterns = [
    path("tag/", TagAPIList.as_view(), name="api-tag-list"),
    path(
        "tag/<str:slug>/",
        TagAPIDetail.as_view(),
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
