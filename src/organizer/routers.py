"""URL Paths and Routers for Organizer App"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    NewsLinkAPIDetail,
    NewsLinkAPIList,
    StartupAPIDetail,
    StartupAPIList,
)
from .viewsets import TagViewSet

api_router = SimpleRouter()
api_router.register("tag", TagViewSet, base_name="api-tag")
api_routes = api_router.urls

urlpatterns = api_routes + [
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
