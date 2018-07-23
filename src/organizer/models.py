"""Django data models for organizing startup company data

Django Model Documentation:
https://docs.djangoproject.com/en/2.1/topics/db/models/
Django Field Reference:
https://docs.djangoproject.com/en/2.1/ref/models/fields/
https://docs.djangoproject.com/en/2.1/ref/models/fields/#charfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#emailfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#slugfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#textfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#urlfield

"""
from django.db import models


class Tag(models.Model):
    """Labels to help categorize data"""

    name = models.CharField(max_length=31)
    slug = models.SlugField()


class Startup(models.Model):
    """Data about a Startup company"""

    name = models.CharField(max_length=31)
    slug = models.SlugField()
    description = models.TextField()
    founded_date = models.DateField()
    contact = models.EmailField()
    website = models.URLField()


class NewsLink(models.Model):
    """Link to external sources about a Startup"""

    title = models.CharField(max_length=63)
    slug = models.SlugField()
    pub_date = models.DateField()
    link = models.URLField()
