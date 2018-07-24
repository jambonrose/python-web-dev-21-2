"""Django data models for news

Django Model Documentation:
https://docs.djangoproject.com/en/2.1/topics/db/models/
https://docs.djangoproject.com/en/2.1/ref/models/options/
https://docs.djangoproject.com/en/2.1/internals/contributing/writing-code/coding-style/#model-style
Django Field Reference:
https://docs.djangoproject.com/en/2.1/ref/models/fields/
https://docs.djangoproject.com/en/2.1/ref/models/fields/#charfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#manytomanyfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#slugfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#textfield

"""
from datetime import date

from django.db import models

from organizer.models import Startup, Tag


class Post(models.Model):
    """Blog post; news article about startups"""

    title = models.CharField(max_length=63)
    slug = models.SlugField(
        max_length=63,
        help_text="A label for URL config",
        unique_for_month="pub_date",
    )
    text = models.TextField()
    pub_date = models.DateField(
        "date published", default=date.today
    )
    tags = models.ManyToManyField(
        Tag, related_name="blog_posts"
    )
    startups = models.ManyToManyField(
        Startup, related_name="blog_posts"
    )

    class Meta:
        get_latest_by = "pub_date"
        ordering = ["-pub_date", "title"]
        verbose_name = "blog post"

    def __str__(self):
        date_string = self.pub_date.strftime("%Y-%m-%d")
        return f"{self.title} on {date_string}"
