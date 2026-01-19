
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from django.contrib.auth.models import User

if not User.objects.filter(username='testuser').exists():
    User.objects.create_superuser('testuser', 'testuser@example.com', 'testpassword')
    print("Superuser 'testuser' created.")
else:
    print("Superuser 'testuser' already exists.")
