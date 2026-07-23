import sys
import os
import traceback
import subprocess

# ── Paths ──────────────────────────────────────────────────────────────
APP_DIR  = '/home/baitmtzi/foot3'
VENV_DIR = '/home/baitmtzi/virtualenv/foot3/3.12'
PYTHON   = os.path.join(VENV_DIR, 'bin', 'python')

# Activate the cPanel-managed virtualenv
activate = os.path.join(VENV_DIR, 'bin', 'activate_this.py')
if os.path.exists(activate):
    exec(open(activate).read(), {'__file__': activate})
else:
    import site
    site.addsitedir(os.path.join(VENV_DIR, 'lib', 'python3.12', 'site-packages'))

# Add project root to sys.path
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# ── Django ─────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talent_platform.settings')
os.environ['DEBUG'] = '0'

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    # Run migrate in background subprocess (non-blocking)
    migrate_flag = os.path.join(APP_DIR, 'tmp', '.migrated')
    if not os.path.exists(migrate_flag):
        log_file = os.path.join(APP_DIR, 'tmp', 'migrate.log')
        with open(log_file, 'w') as log:
            subprocess.Popen(
                [PYTHON, os.path.join(APP_DIR, 'manage.py'), 'migrate', '--noinput'],
                cwd=APP_DIR,
                stdout=log,
                stderr=log,
                start_new_session=True,
            )
        # Create flag so we don't re-run on every request
        try:
            open(migrate_flag, 'w').write('done')
        except:
            pass

except Exception as e:
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
