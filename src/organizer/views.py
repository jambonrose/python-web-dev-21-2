"""Views for Organizer App"""
from django.http import HttpResponse
from django.views import View


class HelloWorld(View):
    """Demonstrate HTTP Request/Response"""

    def get(self, request):
        """Handle GET HTTP method"""
        # HttpResponse defaults:
        # - status code of 200
        # - content-type of "text/html"
        # - encoding "charset=utf-8"
        return HttpResponse("Hello World")
