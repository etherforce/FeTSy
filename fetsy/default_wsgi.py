"""
WSGI config.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

# import site

DJANGO_SETTINGS_MODULE = ''

# FETSY_HOME = '/path/to/FeTSy'
# site.addsitedir(FETSY_HOME)
# site.addsitedir(os.path.join(
#     FETSY_HOME, '.virtualenv', 'lib', 'python3.4', 'site-packages'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)

from django.core.wsgi import get_wsgi_application  # flake8:noqa isort:skip

application = get_wsgi_application()
