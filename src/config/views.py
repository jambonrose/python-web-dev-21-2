"""Site Views

(Views that do not belong in any app but are needed by site.)

I'm breaking the rules here for simplicity: this should not
be in config, as this is not configuration for the project.
However, introducing an app specifically for a single view
would overcomplicate the work we're doing, so it's going
here instead.
"""

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class RootApiView(APIView):
    """Direct users to other API endpoints"""

    def get(self, request, *args, **kwargs):
        """Build & display links to other endpoints"""
        api_endpoints = [
            # (name, url_name),
            ("tag", "api-tag-list"),
            ("startup", "api-startup-list"),
            ("newslink", "api-newslink-list"),
            ("blog", "api-post-list"),
        ]
        data = {
            name: reverse(
                url_name,
                request=request,
                format=kwargs.get("format", None),
            )
            for (name, url_name) in api_endpoints
        }
        return Response(data=data, status=HTTP_200_OK)
