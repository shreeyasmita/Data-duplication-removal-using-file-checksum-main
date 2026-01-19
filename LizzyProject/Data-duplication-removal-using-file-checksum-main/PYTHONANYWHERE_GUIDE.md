# PythonAnywhere Deployment Guide

## Complete Step-by-Step Guide to Deploy Your Django App on PythonAnywhere

PythonAnywhere is a beginner-friendly Python hosting platform perfect for Django applications. This guide will walk you through the entire deployment process.

---

## Step 1: Create a PythonAnywhere Account

1. Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click **"Pricing & signup"**
3. Choose the **"Create a Beginner account"** (Free tier)
4. Complete the registration process
5. Log in to your dashboard

**Free Tier Includes:**
- One web app at `yourusername.pythonanywhere.com`
- 512 MB disk space
- Always-on task capability
- SSH access

---

## Step 2: Upload Your Code

### Option A: Using Git (Recommended)

1. Open a **Bash console** from your PythonAnywhere dashboard
2. Clone your repository:

```bash
git clone https://github.com/yourusername/your-repo.git
# OR if you haven't pushed to Git yet, you'll need to use Option B
```

### Option B: Upload Files Directly

1. Go to the **"Files"** tab in your PythonAnywhere dashboard
2. Create a new directory: `Data-duplication-removal-using-file-checksum-main`
3. Upload your project files using the web interface
   - You can upload a ZIP file and extract it
   - Or use SCP from your local machine:
   
```bash
# From your local machine (requires SSH - available in paid plans)
scp -r Data-duplication-removal-using-file-checksum-main yourusername@ssh.pythonanywhere.com:/home/yourusername/
```

---

## Step 3: Set Up Virtual Environment

From your **Bash console** on PythonAnywhere:

```bash
# Navigate to your project directory
cd Data-duplication-removal-using-file-checksum-main

# Create a virtual environment
mkvirtualenv --python=/usr/bin/python3.10 myproject

# The virtual environment will be automatically activated
# You should see (myproject) in your prompt

# Install dependencies
pip install -r requirements.txt
```

**Note:** If `mkvirtualenv` doesn't work, use:
```bash
python3.10 -m venv ~/.virtualenvs/myproject
source ~/.virtualenvs/myproject/bin/activate
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create your `.env` file:

```bash
cd ~/Data-duplication-removal-using-file-checksum-main
nano .env
```

Add these configurations (use arrow keys to navigate, Ctrl+O to save, Ctrl+X to exit):

```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com

# Database (SQLite for free tier)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/home/yourusername/Data-duplication-removal-using-file-checksum-main/myproject/db.sqlite3

# Email Configuration (update with your credentials)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security Settings
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Generate a new SECRET_KEY:**
```bash
python3.10 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## Step 5: Set Up the Database

```bash
cd ~/Data-duplication-removal-using-file-checksum-main/myproject

# Make sure your virtual environment is activated
workon myproject

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
# Follow the prompts to set username, email, and password

# Collect static files
python manage.py collectstatic --noinput
```

---

## Step 6: Configure the Web App

1. Go to the **"Web"** tab in your PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"** (NOT Django wizard)
4. Select **Python 3.10**
5. Click **Next** until your web app is created

### Configure the Web App Settings:

#### A. Source Code Section
- **Source code:** `/home/yourusername/Data-duplication-removal-using-file-checksum-main/myproject`

#### B. Virtualenv Section
- **Virtualenv:** `/home/yourusername/.virtualenvs/myproject`

#### C. WSGI Configuration File

1. Click on the WSGI configuration file link (it will be something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
2. **Delete all existing content** in the file
3. Copy and paste the content from your `pythonanywhere_wsgi.py` file
4. **Replace `yourusername`** with your actual PythonAnywhere username (appears 3 times)
5. Save the file (Ctrl+S or click Save button)

**The WSGI file should look like this (with your username):**

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOURUSERNAME/Data-duplication-removal-using-file-checksum-main/myproject'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Load environment variables from .env file
from pathlib import Path
env_path = Path('/home/YOURUSERNAME/Data-duplication-removal-using-file-checksum-main') / '.env'
if env_path.exists():
    from decouple import Config, RepositoryEnv
    config = Config(RepositoryEnv(str(env_path)))

# Import Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## Step 7: Configure Static Files

In the **Web** tab, scroll down to the **"Static files"** section:

Add these two mappings:

1. **Static Files:**
   - URL: `/static/`
   - Directory: `/home/yourusername/Data-duplication-removal-using-file-checksum-main/myproject/staticfiles`

2. **Media Files:**
   - URL: `/images/`
   - Directory: `/home/yourusername/Data-duplication-removal-using-file-checksum-main/myproject/uploads`

Click the **green checkmarks** to save each mapping.

---

## Step 8: Create Required Directories

From your Bash console:

```bash
cd ~/Data-duplication-removal-using-file-checksum-main/myproject

# Create uploads directory for user files
mkdir -p uploads

# Verify staticfiles directory exists
ls -la staticfiles/
```

---

## Step 9: Reload Your Web App

1. Go back to the **"Web"** tab
2. Scroll to the top
3. Click the big green **"Reload"** button
4. Wait for the reload to complete

---

## Step 10: Test Your Application

1. Click on your app URL: `https://yourusername.pythonanywhere.com`
2. Your Django app should now be live!

**Test these pages:**
- Main page: `https://yourusername.pythonanywhere.com/`
- Admin panel: `https://yourusername.pythonanywhere.com/admin`
- Login page: `https://yourusername.pythonanywhere.com/login`

---

## Troubleshooting

### 1. Getting Error 500 or "Something went wrong"

**Check the error log:**
1. Go to **"Web"** tab
2. Click on **"Error log"** link
3. Read the last few lines for error details

**Common issues:**
- Wrong paths in WSGI file (check username)
- Missing dependencies (reinstall: `pip install -r requirements.txt`)
- Database not migrated (run migrations again)
- `.env` file not found or has errors

### 2. Static Files Not Loading (No CSS)

```bash
# From Bash console
cd ~/Data-duplication-removal-using-file-checksum-main/myproject
workon myproject
python manage.py collectstatic --noinput
```

Then reload your web app.

### 3. "DisallowedHost" Error

Update your `.env` file:
```env
ALLOWED_HOSTS=yourusername.pythonanywhere.com,localhost,127.0.0.1
```

Then reload your web app.

### 4. Virtual Environment Not Found

```bash
# Create it manually
python3.10 -m venv ~/.virtualenvs/myproject
source ~/.virtualenvs/myproject/bin/activate
pip install -r requirements.txt
```

### 5. Database Locked Error

```bash
# Give proper permissions
chmod 664 ~/Data-duplication-removal-using-file-checksum-main/myproject/db.sqlite3
chmod 775 ~/Data-duplication-removal-using-file-checksum-main/myproject
```

### 6. Import Errors

Make sure all dependencies are installed:
```bash
workon myproject
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Post-Deployment Tasks

### Create Initial Groups and Permissions

From your Bash console:

```bash
cd ~/Data-duplication-removal-using-file-checksum-main/myproject
workon myproject

# Run the setup scripts
python create_user.py
python fix_groups.py
```

### Set Up Email (For Password Reset)

1. Use Gmail App Password (not your regular password)
2. Enable 2FA on your Google account
3. Generate an App Password: https://myaccount.google.com/apppasswords
4. Update `.env` with your app password
5. Reload your web app

---

## Updating Your Application

When you make changes to your code:

```bash
# From Bash console
cd ~/Data-duplication-removal-using-file-checksum-main

# Activate virtual environment
workon myproject

# Pull latest changes (if using Git)
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Run migrations if models changed
cd myproject
python manage.py makemigrations
python manage.py migrate

# Collect static files if changed
python manage.py collectstatic --noinput

# Go to Web tab and click Reload
```

---

## Database Backup

### Backup Your Database

```bash
cd ~/Data-duplication-removal-using-file-checksum-main/myproject
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d)
```

### Download Backup to Local Machine

1. Go to **"Files"** tab
2. Navigate to your database file
3. Click on the file
4. Click **"Download"** button

---

## Monitoring and Logs

### View Error Logs
- **Web** tab → **Error log** link
- Shows Python errors and Django debug output

### View Access Logs
- **Web** tab → **Access log** link
- Shows all HTTP requests to your app

### View Console Output
- Any `print()` statements appear in the error log

---

## Upgrading to Paid Plan

Free tier limitations:
- One web app only
- No scheduled tasks
- No always-on workers
- Limited CPU time
- No SSH access (in some regions)

Consider upgrading if you need:
- Multiple web apps
- More storage
- Scheduled tasks (cron jobs)
- Background workers
- SSH access
- More CPU power

Plans start at $5/month: https://www.pythonanywhere.com/pricing/

---

## Security Best Practices

- ✅ Keep `DEBUG=False` in production
- ✅ Use strong `SECRET_KEY`
- ✅ Never commit `.env` file to Git
- ✅ Use Gmail App Passwords, not regular passwords
- ✅ Regularly update dependencies: `pip install --upgrade -r requirements.txt`
- ✅ Regularly backup your database
- ✅ Monitor error logs for suspicious activity

---

## Useful Commands Reference

```bash
# Activate virtual environment
workon myproject

# Deactivate virtual environment
deactivate

# List all virtual environments
lsvirtualenv

# Django management commands
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py shell

# Check Python version
python --version

# List installed packages
pip list

# Install specific package
pip install package-name

# Update requirements file
pip freeze > requirements.txt
```

---

## Additional Resources

- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **PythonAnywhere Forums:** https://www.pythonanywhere.com/forums/
- **Django Documentation:** https://docs.djangoproject.com/
- **Django Deployment Checklist:** https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

---

## Support

### PythonAnywhere Support
- Free users: Forum support
- Paid users: Email support
- Help pages: https://help.pythonanywhere.com/

### Common Issues Documentation
- Database issues: https://help.pythonanywhere.com/pages/DebuggingDatabaseIssues
- Static files: https://help.pythonanywhere.com/pages/DjangoStaticFiles
- WSGI configuration: https://help.pythonanywhere.com/pages/DebuggingImportError

---

## Quick Checklist

Before going live, make sure you've:

- [ ] Created PythonAnywhere account
- [ ] Uploaded all project files
- [ ] Created virtual environment
- [ ] Installed all dependencies from requirements.txt
- [ ] Created and configured .env file
- [ ] Run database migrations
- [ ] Created superuser account
- [ ] Collected static files
- [ ] Configured Web app settings
- [ ] Updated WSGI configuration file
- [ ] Added static files mappings
- [ ] Reloaded web app
- [ ] Tested main page loads
- [ ] Tested admin panel works
- [ ] Tested user login/registration
- [ ] Tested file upload functionality
- [ ] Set up email configuration

---

**Your Django Data Deduplication application is now live on PythonAnywhere!** 🎉

Access it at: `https://yourusername.pythonanywhere.com`
