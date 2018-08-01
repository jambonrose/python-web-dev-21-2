import django.db.models.deletion
from django.db import migrations, models
from django_extensions.db.fields import AutoSlugField


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=31, unique=True
                    ),
                ),
                (
                    "slug",
                    AutoSlugField(
                        blank=True,
                        editable=False,
                        help_text="A label for URL config.",
                        max_length=31,
                        populate_from=["name"],
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Startup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=31
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="A label for URL config.",
                        max_length=31,
                        unique=True,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "founded_date",
                    models.DateField(
                        verbose_name="date founded"
                    ),
                ),
                (
                    "contact",
                    models.EmailField(max_length=254),
                ),
                (
                    "website",
                    models.URLField(max_length=255),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        to="organizer.Tag"
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "get_latest_by": "founded_date",
            },
        ),
        migrations.CreateModel(
            name="NewsLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=63)),
                ("slug", models.SlugField(max_length=63)),
                (
                    "pub_date",
                    models.DateField(
                        verbose_name="date published"
                    ),
                ),
                ("link", models.URLField(max_length=255)),
                (
                    "startup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organizer.Startup",
                    ),
                ),
            ],
            options={
                "verbose_name": "news article",
                "ordering": ["-pub_date"],
                "get_latest_by": "pub_date",
            },
        ),
        migrations.AlterUniqueTogether(
            name="newslink",
            unique_together={("slug", "startup")},
        ),
    ]
