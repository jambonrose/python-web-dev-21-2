"""Django data models for news

Django Model Documentation:
https://docs.djangoproject.com/en/2.1/topics/db/models/
Django Field Reference:
https://docs.djangoproject.com/en/2.1/ref/models/fields/
https://docs.djangoproject.com/en/2.1/ref/models/fields/#charfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#manytomanyfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#slugfield
https://docs.djangoproject.com/en/2.1/ref/models/fields/#textfield

"""
from django.db import models

from organizer.models import Startup, Tag


class Post(models.Model):
    """Blog post; news article about startups"""

    title = models.CharField(max_length=63)
    slug = models.SlugField()
    text = models.TextField()
    pub_date = models.DateField()
    tags = models.ManyToManyField(Tag)
    startups = models.ManyToManyField(Startup)
