"""Views for Organizer App"""
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import NewsLinkForm, StartupForm, TagForm
from .models import NewsLink, Startup, Tag


class NewsLinkObjectMixin:
    """Django View mix-in to find NewsLinks"""

    def get_object(self):
        """Get NewsLink from database"""
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
            NewsLink,
            startup__slug=startup_slug,
            slug=newslink_slug,
        )


class NewsLinkContextMixin:
    """Build template context for NewsLink views"""

    def get_context_data(self, **kwargs):
        """Build context dictionary for template"""
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        context = {"startup": startup}
        context.update(kwargs)
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context


class VerifyStartupFkToUriMixin:
    """Mixin to verify Startup data in NewsLink views

    NewsLink creation and updating views specify the Startup slug in the URI.
    However, for simplicity when interacting with the NewsLinkForm, the form
    also has a field for the Startup object. This class ensures that the
    Startup referred to by the URI and by the NewsLinkForm field is one and
    the same
    """

    def verify_startup_fk_matches_uri(
        self, request, startup
    ):
        """Raise HTTP 400 if Startup data mismatched"""
        if str(startup.pk) != request.POST.get("startup"):
            raise SuspiciousOperation(
                "Startup Form PK and URI do not match"
            )


class NewsLinkCreate(
    VerifyStartupFkToUriMixin, NewsLinkContextMixin, View
):
    """Create a link to an article about a startup"""

    extra_context = {"update": False}
    template_name = "newslink/form.html"

    def get_initial(self):
        """Pre-select Startup in NewsLinkForm"""
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        return {"startup": startup.pk}

    def get(self, request, startup_slug):
        """Display form to create new NewsLinks"""
        context = self.get_context_data(
            form=NewsLinkForm(initial=self.get_initial())
        )
        return render(request, self.template_name, context)

    def post(self, request, startup_slug):
        """Process form submission with new NewsLink data"""
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        self.verify_startup_fk_matches_uri(request, startup)
        newslink_form = NewsLinkForm(request.POST)
        if newslink_form.is_valid():
            newslink = newslink_form.save()
            return redirect(newslink)
        context = self.get_context_data(form=newslink_form)
        return render(request, self.template_name, context)


class NewsLinkDelete(
    NewsLinkObjectMixin, NewsLinkContextMixin, View
):
    """Delete a link to an article about a startup"""

    extra_context = None
    template_name = "newslink/confirm_delete.html"

    def get(self, request, startup_slug, newslink_slug):
        """Ask for confirmation of deletion"""
        newslink = self.get_object()
        context = self.get_context_data(newslink=newslink)
        return render(request, self.template_name, context)

    def post(self, request, startup_slug, newslink_slug):
        """Delete specified NewsLink"""
        newslink = self.get_object()
        newslink.delete()
        startup = get_object_or_404(
            Startup, slug=startup_slug
        )
        return redirect(startup)


class NewsLinkDetail(NewsLinkObjectMixin, View):
    """Redirect /<startup>/<newslink>/ to /<startup>/"""

    def get(self, request, startup_slug, newslink_slug):
        """Redirect user to Startup page"""
        # We could redirect like so:
        #
        #     return redirect(
        #         reverse(
        #             "startup_detail",
        #             kwargs={"slug": startup_slug},
        #         )
        #     )
        #
        # The advantage of the code above is that we avoid a
        # database query.
        #
        # However, this means we will not show a 404 if the
        # NewsLink slug does not exist. For correctness, we
        # therefore check the existence of the NewsLink, and
        # then redirect.
        newslink = self.get_object()
        # NewsLink.get_absolute_url returns the detail page
        # of startup, so we could use:
        #     return redirect(newslink)
        #
        # However, it may also be surprising/confusing, so
        # we opt instead for the code below.
        return redirect(newslink.startup)


class NewsLinkUpdate(
    VerifyStartupFkToUriMixin,
    NewsLinkObjectMixin,
    NewsLinkContextMixin,
    View,
):
    """Update a link to an article about a startup"""

    extra_context = {"update": True}
    template_name = "newslink/form.html"

    def get(self, request, startup_slug, newslink_slug):
        """Display pre-filled form to update NewsLink"""
        newslink = self.get_object()
        context = self.get_context_data(
            form=NewsLinkForm(instance=newslink),
            newslink=newslink,
        )
        return render(request, self.template_name, context)

    def post(self, request, startup_slug, newslink_slug):
        """Process form submission with NewsLink data"""
        newslink = self.get_object()
        startup = newslink.startup
        self.verify_startup_fk_matches_uri(request, startup)
        newslink_form = NewsLinkForm(
            request.POST, instance=newslink
        )
        if newslink_form.is_valid():
            newslink = newslink_form.save()
            return redirect(newslink)
        context = self.get_context_data(
            form=newslink_form, newslink=newslink
        )
        return render(request, self.template_name, context)


class TagList(ListView):
    """Display a list of Tags"""

    queryset = Tag.objects.all()
    template_name = "tag/list.html"


class TagDetail(DetailView):
    """Display a single Tag"""

    queryset = Tag.objects.all()
    template_name = "tag/detail.html"


class TagCreate(CreateView):
    """Create new Tags via HTML form"""

    form_class = TagForm
    model = Tag
    template_name = "tag/form.html"
    extra_context = {"update": False}


class TagUpdate(UpdateView):
    """Update a Tag via HTML form"""

    form_class = TagForm
    model = Tag
    template_name = "tag/form.html"
    extra_context = {"update": True}


class TagDelete(DeleteView):
    """Confirm and delete a Tag via HTML Form"""

    model = Tag
    template_name = "tag/confirm_delete.html"
    success_url = reverse_lazy("tag_list")


class StartupCreate(CreateView):
    """Create new Startups via HTML form"""

    form_class = StartupForm
    model = Startup
    template_name = "startup/form.html"
    extra_context = {"update": False}


class StartupDelete(DeleteView):
    """Confirm and delete a Startup via HTML Form"""

    model = Startup
    template_name = "startup/confirm_delete.html"
    success_url = reverse_lazy("startup_list")


class StartupList(ListView):
    """Display a list of Startups"""

    queryset = Startup.objects.all()
    template_name = "startup/list.html"


class StartupDetail(DetailView):
    """Display a single Startup"""

    queryset = Startup.objects.all()
    template_name = "startup/detail.html"


class StartupUpdate(UpdateView):
    """Update a Startup via HTML form"""

    form_class = StartupForm
    model = Startup
    template_name = "startup/form.html"
    extra_context = {"update": True}
