"""Django Settings for Production instances of the site"""
from .base import *  # noqa: F401 F403

######################################################################
# PRODUCTION SETTINGS
######################################################################

ALLOWED_HOSTS = [".herokuapp.com"]

ADMINS = MANAGERS = [
    # ('Your Name', 'name@email.com'),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

#####################
# SECURITY SETTINGS #
#####################

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SESSION_COOKIE_DOMAIN = None  # not set on subdomains
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "suorganizer_sessionid"
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

X_FRAME_OPTIONS = "DENY"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    )
}
