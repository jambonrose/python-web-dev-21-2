"""Mix-in classes for Organizer Views"""
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404

from .models import NewsLink, Startup


class NewsLinkContextMixin:
    """Add Startup to template context in NewsLink views"""

    def get_context_data(self, **kwargs):
        """Dynamically add to template context

        http://ccbv.co.uk/ContextMixin
        """
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        return super().get_context_data(
            startup=startup, **kwargs
        )


class NewsLinkObjectMixin:
    """Django View mix-in to find NewsLinks"""

    model = NewsLink

    def get_object(self, queryset=None):
        """Get NewsLink from database

        http://ccbv.co.uk/SingleObjectMixin
        """
        if queryset is None:
            if hasattr(self, "get_queryset"):
                queryset = self.get_queryset()
            else:
                queryset = self.model.objects.all()

        # Django's View class puts URI kwargs in dictionary
        startup_slug = self.kwargs.get("startup_slug")
        newslink_slug = self.kwargs.get("newslink_slug")

        if startup_slug is None or newslink_slug is None:
            raise AttributeError(
                f"View {self.__class__.__name__} must be"
                f"called with a slug for a Startup and a"
                f"slug for a NewsLink objects."
            )

        return get_object_or_404(
            queryset,
            startup__slug=startup_slug,
            slug=newslink_slug,
        )


class VerifyStartupFkToUriMixin:
    """Mixin to verify Startup data in NewsLink views

    NewsLink views to create and update specify the Startup
    slug in the URI.  However, for simplicity when
    interacting with the NewsLinkForm, the form also has a
    field for the Startup object. This class ensures that
    the Startup referred to by the URI and by the
    NewsLinkForm field is one and the same.
    """

    def verify_startup_fk_matches_uri(self):
        """Raise HTTP 400 if Startup data mismatched"""
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        form_startup_pk = self.request.POST.get("startup")
        if str(startup.pk) != form_startup_pk:
            raise SuspiciousOperation(
                "Startup Form PK and URI do not match"
            )

    def post(self, request, *args, **kwargs):
        """Check Startup data before form submission process

        - Raise HTTP 400 if Startup data mismatched
        - Hook into Generic Views for rest of work
        """
        self.verify_startup_fk_matches_uri()
        return super().post(request, *args, **kwargs)
