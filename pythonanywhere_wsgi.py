"""
WSGI config for PythonAnywhere deployment

This file is used by PythonAnywhere to serve your Django application.
Replace 'yourusername' with your actual PythonAnywhere username.
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/Data-duplication-removal-using-file-checksum-main/myproject'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where your settings module is
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Load environment variables from .env file
from pathlib import Path
env_path = Path('/home/yourusername/Data-duplication-removal-using-file-checksum-main') / '.env'
if env_path.exists():
    from decouple import Config, RepositoryEnv
    config = Config(RepositoryEnv(str(env_path)))

# Activate your virtual environment
activate_this = '/home/yourusername/.virtualenvs/myproject/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
