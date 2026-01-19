import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User as A_U, Group
from ddp.models import User

# Create a regular user
username = 'regularuser'
email = 'user@example.com'
password = 'user123'

# Check if user already exists
if not A_U.objects.filter(username=username).exists():
    # Create Django auth user
    auth_user = A_U.objects.create_user(username=username, email=email, password=password)
    
    # Add to user group
    user_group = Group.objects.get(name='user')
    auth_user.groups.add(user_group)
    
    # Create User model entry
    ddp_user = User(name=username)
    ddp_user.save()
    
    print(f"✅ Regular user created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    print(f"\nYou can now login and upload files at: http://127.0.0.1:8000/login/")
else:
    print(f"User '{username}' already exists!")
    print(f"Username: {username}")
    print(f"Password: {password}")
