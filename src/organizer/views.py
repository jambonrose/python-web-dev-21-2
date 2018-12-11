"""Views for Organizer App"""
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


class NewsLinkCreate(View):
    """Create a link to an article about a startup"""

    template_name = "newslink/form.html"

    def get(self, request, startup_slug):
        """Display form to create new NewsLinks"""
        startup = get_object_or_404(
            Startup, slug=startup_slug
        )
        context = {
            "form": NewsLinkForm(),
            "startup": startup,
            "update": False,
        }
        return render(request, self.template_name, context)

    def post(self, request, startup_slug):
        """Process form submission with new NewsLink data"""
        newslink_form = NewsLinkForm(request.POST)
        if newslink_form.is_valid():
            newslink = newslink_form.save()
            return redirect(newslink)
        startup = get_object_or_404(
            Startup, slug=startup_slug
        )
        context = {
            "form": newslink_form,
            "startup": startup,
            "update": False,
        }
        return render(request, self.template_name, context)


class NewsLinkDelete(View):
    """Delete a link to an article about a startup"""

    template_name = "newslink/confirm_delete.html"

    def get_object(self):
        """Get NewsLink from database"""
        # Django's View class puts URI kwargs in dictionary
        startup_slug = self.kwargs.get("startup_slug")
        newslink_slug = self.kwargs.get("newslink_slug")

        return get_object_or_404(
            NewsLink,
            startup__slug=startup_slug,
            slug=newslink_slug,
        )

    def get(self, request, startup_slug, newslink_slug):
        """Ask for confirmation of deletion"""
        newslink = self.get_object()
        context = {
            "newslink": newslink,
            "startup": newslink.startup,
        }
        return render(request, self.template_name, context)

    def post(self, request, startup_slug, newslink_slug):
        """Delete specified NewsLink"""
        newslink = self.get_object()
        newslink.delete()
        startup = get_object_or_404(
            Startup, slug=startup_slug
        )
        return redirect(startup)


class NewsLinkDetail(View):
    """Redirect /<startup>/<newslink>/ to /<startup>/"""

    def get_object(self):
        """Get NewsLink from database"""
        # Django's View class puts URI kwargs in dictionary
        startup_slug = self.kwargs.get("startup_slug")
        newslink_slug = self.kwargs.get("newslink_slug")

        return get_object_or_404(
            NewsLink,
            startup__slug=startup_slug,
            slug=newslink_slug,
        )

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


class NewsLinkUpdate(View):
    """Update a link to an article about a startup"""

    template_name = "newslink/form.html"

    def get_object(self):
        """Get NewsLink from database"""
        # Django's View class puts URI kwargs in dictionary
        startup_slug = self.kwargs.get("startup_slug")
        newslink_slug = self.kwargs.get("newslink_slug")

        return get_object_or_404(
            NewsLink,
            startup__slug=startup_slug,
            slug=newslink_slug,
        )

    def get(self, request, startup_slug, newslink_slug):
        """Display pre-filled form to update NewsLink"""
        newslink = self.get_object()
        context = {
            "form": NewsLinkForm(instance=newslink),
            "newslink": newslink,
            "startup": newslink.startup,
            "update": True,
        }
        return render(request, self.template_name, context)

    def post(self, request, startup_slug, newslink_slug):
        """Process form submission with NewsLink data"""
        newslink = self.get_object()
        newslink_form = NewsLinkForm(
            request.POST, instance=newslink
        )
        if newslink_form.is_valid():
            newslink = newslink_form.save()
            return redirect(newslink)
        context = {
            "form": newslink_form,
            "newslink": newslink,
            "startup": newslink.startup,
            "update": True,
        }
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
