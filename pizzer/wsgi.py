"""
WSGI config for pizzer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

root_path = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(root_path, 'pizzer'))
sys.path.insert(0, root_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizzer.settings')

application = get_wsgi_application()
