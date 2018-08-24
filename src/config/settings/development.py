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
