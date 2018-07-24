"""Django data models for organizing startup company data

Django Model Documentation:
https://docs.djangoproject.com/en/2.1/topics/db/models/
Django Field Reference:
https://docs.djangoproject.com/en/2.1/ref/models/fields/
https://docs.djangoproject.com/en/2.1/ref/models/fields/#charfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#emailfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#foreignkey
https://docs.djangoproject.com/en/2.1/ref/models/fields/#manytomanyfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#slugfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#textfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#urlfield

"""
from django.db import models


class Tag(models.Model):
    """Labels to help categorize data"""

    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(
        max_length=31,
        unique=True,
        help_text="A label for URL config.",
    )

    def __str__(self):
        return self.name


class Startup(models.Model):
    """Data about a Startup company"""

    name = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(
        max_length=31,
        unique=True,
        help_text="A label for URL config.",
    )
    description = models.TextField()
    founded_date = models.DateField("date founded")
    contact = models.EmailField()
    website = models.URLField(
        max_length=255  # https://tools.ietf.org/html/rfc3986
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class NewsLink(models.Model):
    """Link to external sources about a Startup"""

    title = models.CharField(max_length=63)
    slug = models.SlugField(max_length=63)
    pub_date = models.DateField("date published")
    link = models.URLField(
        max_length=255  # https://tools.ietf.org/html/rfc3986
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.startup}: {self.title}"
