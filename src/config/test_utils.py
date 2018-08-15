"""Utility code for tests

I'm breaking the rules here for simplicity: this should not
be in config, as this is not configuration for the project.
However, introducing an app specifically for test utilities
would overcomplicate the work we're doing, so it's going
here instead.

"""
from django.db.models.fields.related import ManyToManyField
from django.test import RequestFactory
from rest_framework.reverse import reverse as rf_reverse


def lmap(*args, **kwargs):
    """Shortcut to return list when mapping"""
    return list(map(*args, **kwargs))


def omit_keys(*args):
    """Remove keys from a dictionary"""
    *keys, dict_obj = args
    return {
        field: value
        for field, value in dict_obj.items()
        if field not in keys
    }


def reverse(name, *args, **kwargs):
    """Shorter Reverse function for the very lazy tester"""
    full_url = kwargs.pop("full", False)
    uri = rf_reverse(name, args=args, kwargs=kwargs)
    if "request" not in kwargs and full_url:
        return f"http://testserver{uri}"
    return uri


def context_kwarg(path):
    """Build context for Serializers

    Not necessary from the outset, but the use of
    Hyperlinked fields and serializers necessitates the
    inclusion of a request. This utility is pre-empting
    that requirement.

    """
    return {
        "context": {"request": RequestFactory().get(path)}
    }


def get_concrete_field_names(Model):
    """Return all of the concrete field names for a Model

    https://docs.djangoproject.com/en/2.1/ref/models/meta/

    """
    return [
        field.name
        for field in Model._meta.get_fields()
        if field.concrete
        and (
            not (
                field.is_relation
                or field.one_to_one
                or (
                    field.many_to_one
                    and field.related_model
                )
            )
        )
    ]


def get_instance_data(model_instance, related_value="pk"):
    """Return a dict of fields for the model_instance instance

    Effectively a simple form of serialization

    """
    from django.db.models import DateField, DateTimeField

    model_fields = model_instance._meta.get_fields()

    # add basic fields
    concrete_fields = [
        field
        for field in model_fields
        if field.concrete
        and not isinstance(
            field, (DateField, DateTimeField)
        )
    ]
    instance_data = {
        field.name: field.value_from_object(model_instance)
        for field in concrete_fields
    }

    # special case for datefields to ensure a string, not an object
    concrete_date_fields = [
        field
        for field in model_fields
        if field.concrete
        and isinstance(field, (DateField, DateTimeField))
    ]
    for field in concrete_date_fields:
        instance_data[field.name] = str(
            field.value_from_object(model_instance)
        )

    # add many-to-many fields
    # the `isinstance` check avoids ManyToManyRel
    m2m_fields = [
        field
        for field in model_fields
        if field.many_to_many
        and isinstance(field, ManyToManyField)
    ]
    if model_instance.pk is None:
        for field in m2m_fields:
            instance_data[field.name] = []
    else:
        for field in m2m_fields:
            instance_data[field.name] = [
                getattr(obj, related_value)
                for obj in field.value_from_object(
                    model_instance
                )
            ]

    return instance_data
