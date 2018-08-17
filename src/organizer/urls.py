"""URL paths for Organizer App"""
from django.urls import path

from .views import (
    StartupDetail,
    StartupList,
    TagDetail,
    TagList,
)

urlpatterns = [
    path(
        "startup/",
        StartupList.as_view(),
        name="startup_list",
    ),
    path(
        "startup/<str:slug>/",
        StartupDetail.as_view(),
        name="startup_detail",
    ),
    path("tag/", TagList.as_view(), name="tag_list"),
    path(
        "tag/<str:slug>/",
        TagDetail.as_view(),
        name="tag_detail",
    ),
]
