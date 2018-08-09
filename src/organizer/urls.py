"""URL Configuration for Organizer App"""
from django.urls import path

from .views import TagAPIDetail, TagAPIList

urlpatterns = [
    path("", TagAPIList.as_view(), name="api-tag-list"),
    path(
        "<str:slug>/",
        TagAPIDetail.as_view(),
        name="api-tag-detail",
    ),
]
