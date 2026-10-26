"""Flask-Erweiterungen, die views.py und die Blueprints gemeinsam nutzen.

Hier angelegt und in views.py mit init_app() an die App gebunden, damit
members.py und admin.py sie importieren koennen, ohne views.py zu
importieren (sonst Zirkelimport).
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

# Zaehler im Arbeitsspeicher: genuegt, solange gunicorn mit einem Worker
# laeuft (docker-compose.prod.yml). Hinter Nginx liefert ProxyFix die echte
# Client-Adresse fuer get_remote_address.
limiter = Limiter(get_remote_address, storage_uri="memory://", default_limits=[])
