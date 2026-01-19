import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User, Group
from ddp.models import User as DDP_User

# Create groups if they don't exist
groups_to_create = ['admin', 'user', 'blocked user']
for group_name in groups_to_create:
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"Group '{group_name}' created.")
    else:
        print(f"Group '{group_name}' already exists.")

# Add testuser to admin group
try:
    testuser = User.objects.get(username='testuser')
    admin_group = Group.objects.get(name='admin')
    testuser.groups.add(admin_group)
    
    # Create DDP User model entry if it doesn't exist
    if not DDP_User.objects.filter(name='testuser').exists():
        ddp_user = DDP_User(name='testuser')
        ddp_user.save()
        print(f"DDP User model entry created for 'testuser'")
    
    print(f"\nUser 'testuser' added to 'admin' group successfully!")
    print(f"User groups: {[g.name for g in testuser.groups.all()]}")
except User.DoesNotExist:
    print("User 'testuser' not found!")
except Exception as e:
    print(f"Error: {e}")
