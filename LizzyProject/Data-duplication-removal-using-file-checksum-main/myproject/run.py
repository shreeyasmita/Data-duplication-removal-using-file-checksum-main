
import os
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management.base import BaseCommand
        # Create a superuser
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_superuser('testuser', 'testuser@example.com', 'testpassword')
            print("Superuser 'testuser' created.")
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(['manage.py', 'runserver'])

if __name__ == '__main__':
    main()
