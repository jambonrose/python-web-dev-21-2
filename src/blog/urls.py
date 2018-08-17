"""URL Configuration for Blog App"""
from django.urls import path

from .views import PostAPIDetail, PostAPIList

urlpatterns = [
    path(
        "blog/", PostAPIList.as_view(), name="api-post-list"
    ),
    path(
        "blog/<int:year>/<int:month>/<str:slug>/",
        PostAPIDetail.as_view(),
        name="api-post-detail",
    ),
]
