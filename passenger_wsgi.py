import sys
import os
import traceback

# ── Paths ──────────────────────────────────────────────────────────────
APP_DIR  = '/home/baitmtzi/foot3'
VENV_DIR = '/home/baitmtzi/virtualenv/foot3/3.12'

# Activate the cPanel-managed virtualenv
activate = os.path.join(VENV_DIR, 'bin', 'activate_this.py')
if os.path.exists(activate):
    exec(open(activate).read(), {'__file__': activate})
else:
    # Fallback: manually inject site-packages
    import site
    site.addsitedir(os.path.join(VENV_DIR, 'lib', 'python3.12', 'site-packages'))

# Add project root to sys.path
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# ── Django ─────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talent_platform.settings')
os.environ['DEBUG'] = '1'  # TEMPORARY: see 500 traceback — revert after fix

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # ✅ Show full traceback so you can diagnose production errors
    _error_body = (
        f'Django startup error:\n\n{e}\n\n'
        f'--- Traceback ---\n{traceback.format_exc()}'
    ).encode('utf-8', errors='replace')

    def application(environ, start_response):
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ('Content-Length', str(len(_error_body))),
        ])
        return [_error_body]
