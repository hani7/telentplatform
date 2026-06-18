import sys
import os

# ── cPanel Passenger WSGI ──
# On cPanel, Passenger automatically activates the managed virtualenv.
# We only need to add the project root to sys.path.

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'talent_platform.settings'
os.environ['DEBUG'] = '0'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
