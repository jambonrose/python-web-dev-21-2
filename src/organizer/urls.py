"""URL paths for Organizer App"""
from django.urls import path

from .views import TagDetail, TagList

urlpatterns = [
    path("tag/", TagList.as_view(), name="tag_list"),
    path(
        "tag/<str:slug>/",
        TagDetail.as_view(),
        name="tag_detail",
    ),
]
