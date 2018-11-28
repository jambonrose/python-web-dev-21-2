"""URL Paths and Routers for Blog App"""
from rest_framework.routers import SimpleRouter

from .viewsets import PostViewSet


class PostRouter(SimpleRouter):
    """Override the SimpleRouter for blog posts

    DRF's routers expect there to only be a single variable
    for finding objects. However, our blog posts needs
    three! We therefore override the Router's behavior to
    make it do what we want.

    The big question: was it worth switching to a ViewSet
    and Router over our previous config for this?
    """

    def get_lookup_regex(self, *args, **kwargs):
        """Return regular expression pattern for URL path

        This is the equivalent of the simple path:
            <int:year>/<int:month>/<str:slug>
        """
        return (
            r"(?P<year>\d+)/"
            r"(?P<month>\d+)/"
            r"(?P<slug>[\w\-]+)"
        )


post_router = PostRouter()
post_router.register(
    "blog", PostViewSet, base_name="api-post"
)
urlpatterns = post_router.urls
