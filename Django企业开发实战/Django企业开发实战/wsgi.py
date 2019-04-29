"""
WSGI config for Django企业开发实战 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
profile = os.environ.get('TYPEIDEA_PROFILE','develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django企业开发实战.settings.%s"%profile)

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django企业开发实战.settings")

application = get_wsgi_application()
