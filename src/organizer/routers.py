"""URL Paths and Routers for Organizer App"""
from rest_framework.routers import SimpleRouter

from .viewsets import (
    NewsLinkViewSet,
    StartupViewSet,
    TagViewSet,
)


class NewsLinkRouter(SimpleRouter):
    """Override the SimpleRouter for articles

    DRF's routers expect there to only be a single variable
    for finding objects. However, our NewsLinks needs
    two! We therefore override the Router's behavior to
    make it do what we want.

    The big question: was it worth switching to a ViewSet
    and Router over our previous config for this?
    """

    def get_lookup_regex(self, *args, **kwargs):
        """Return regular expression pattern for URL path

        This is the (rough) equivalent of the simple path:
            <str:startup_slug>/<str:newslink_slug>
        """
        return (
            r"(?P<startup_slug>[^/.]+)/"
            r"(?P<newslink_slug>[^/.]+)"
        )


api_router = SimpleRouter()
api_router.register("tag", TagViewSet, base_name="api-tag")
api_router.register(
    "startup", StartupViewSet, base_name="api-startup"
)

nl_router = NewsLinkRouter()
nl_router.register(
    "newslink", NewsLinkViewSet, base_name="api-newslink"
)

urlpatterns = api_router.urls + nl_router.urls
