"""Django data models for organizing startup company data

Django Model Documentation:
https://docs.djangoproject.com/en/2.1/topics/db/models/
Django Field Reference:
https://docs.djangoproject.com/en/2.1/ref/models/fields/

"""
from django.db import models


class Tag(models.Model):
    """Labels to help categorize data"""

    pass


class Startup(models.Model):
    """Data about a Startup company"""

    pass


class NewsLink(models.Model):
    """Link to external sources about a Startup"""

    pass
