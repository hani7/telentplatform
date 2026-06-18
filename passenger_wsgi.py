import sys
import os

# ── cPanel Python App – passenger_wsgi.py ──
# This file MUST be in the root of your app directory on cPanel.
# App root = the folder cPanel set when you created the Python app.

# 1) Add the project root to sys.path so Django can be found
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

# 2) Point to the cPanel-managed virtualenv (cPanel creates it automatically)
#    The venv is usually at ~/virtualenv/<appname>/<python_version>/lib/...
#    cPanel activates it for us, but we add it explicitly as fallback.
for py_ver in ('3.12', '3.13', '3.11', '3.10'):
    site_pkgs = os.path.join(APP_DIR, 'env', 'lib', f'python{py_ver}', 'site-packages')
    if os.path.isdir(site_pkgs):
        sys.path.insert(0, site_pkgs)
        break

# 3) Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'talent_platform.settings'
os.environ['DEBUG'] = '0'

# 4) Load .env file if present (python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(APP_DIR, '.env'))
except ImportError:
    pass

# 5) Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
