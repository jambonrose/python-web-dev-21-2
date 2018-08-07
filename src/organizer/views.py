"""Views for Organizer App"""
from django.http import HttpResponse
from django.views.decorators.http import (
    require_http_methods
)


# equivalent to require_safe decorator
@require_http_methods(["GET", "HEAD"])
def hello_world(request):
    """Demonstrate HTTP Request/Response"""
    # HttpResponse defaults:
    # - status code of 200
    # - content-type of "text/html"
    # - encoding "charset=utf-8"
    return HttpResponse("Hello World")
