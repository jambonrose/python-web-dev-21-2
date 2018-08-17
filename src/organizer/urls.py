"""URL paths for Organizer App"""
from django.urls import path

from .views import tag_detail, tag_list

urlpatterns = [
    path("tag/", tag_list, name="tag_list"),
    path("tag/<str:slug>/", tag_detail, name="tag_detail"),
]
