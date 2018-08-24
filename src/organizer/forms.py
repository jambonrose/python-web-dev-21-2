"""Forms for the Organizer app"""
from django.forms import CharField, Form, SlugField

from .models import Tag


class TagForm(Form):
    """HTML form for Tag objects"""

    name = CharField(max_length=31)
    slug = SlugField(
        help_text="A label for URL config",
        max_length=31,
        required=False,
    )

    def save(self):
        """Save the data in the bound form"""
        return Tag.objects.create(
            name=self.cleaned_data["name"],
            slug=self.cleaned_data["slug"],
        )
