"""Factory classes for blog models"""
from factory import DjangoModelFactory, Faker

from ..models import Post


class PostFactory(DjangoModelFactory):
    """Factory for Blog Post data"""

    title = Faker(
        "sentence", nb_words=3, variable_nb_words=True
    )
    slug = Faker("slug")
    text = Faker(
        "paragraph",
        nb_sentences=3,
        variable_nb_sentences=True,
    )
    pub_date = Faker("date_this_decade", before_today=True)

    class Meta:
        model = Post
