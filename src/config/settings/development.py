"""Development settings for Startup Organizer"""
from .base import *  # noqa: F403

DEBUG = ENV.bool("DEBUG", default=True)  # noqa: F405

TEMPLATES[0]["OPTIONS"].update(  # noqa: F405
    {
        "debug": ENV.bool(  # noqa: F405
            "TEMPLATE_DEBUG", default=True
        )
    }
)

# https://github.com/evansd/whitenoise/issues/191
# Normally set to settings.DEBUG, but tests run with DEBUG=FALSE!
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True
