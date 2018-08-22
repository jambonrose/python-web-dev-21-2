"""URL Paths and Routers for Organizer App"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import NewsLinkAPIDetail, NewsLinkAPIList
from .viewsets import StartupViewSet, TagViewSet

api_router = SimpleRouter()
api_router.register("tag", TagViewSet, base_name="api-tag")
api_router.register(
    "startup", StartupViewSet, base_name="api-startup"
)
api_routes = api_router.urls

urlpatterns = api_routes + [
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
