# VPS Deployment Guide for Django Data Deduplication Application

This guide will walk you through deploying your Django application on a VPS (Ubuntu/Debian).

## Prerequisites

- A VPS server (Ubuntu 20.04 or later recommended)
- SSH access to your server
- A domain name (optional but recommended)
- Basic knowledge of Linux command line

## Quick Start (Automated Deployment)

1. **Upload your project to the server:**
   ```bash
   # On your local machine
   scp -r Data-duplication-removal-using-file-checksum-main username@your-server-ip:/home/username/
   ```

2. **SSH into your server:**
   ```bash
   ssh username@your-server-ip
   ```

3. **Run the deployment script:**
   ```bash
   cd Data-duplication-removal-using-file-checksum-main
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Follow the prompts** and configure your `.env` file when prompted.

---

## Manual Deployment Steps

If you prefer to deploy manually or the automated script fails, follow these steps:

### Step 1: Update System and Install Dependencies

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib
```

### Step 2: Setup PostgreSQL Database

```bash
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
CREATE DATABASE ddp_database;
CREATE USER ddp_user WITH PASSWORD 'your_password_here';
ALTER ROLE ddp_user SET client_encoding TO 'utf8';
ALTER ROLE ddp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ddp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ddp_database TO ddp_user;
\q
```

### Step 3: Upload and Setup Project

```bash
# Create project directory
mkdir -p /home/$USER/ddp-app
cd /home/$USER/ddp-app

# Upload your project files here (use scp, git clone, or sftp)
# Assuming files are in current directory

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit the .env file
nano .env
```

Update these critical settings:
```env
SECRET_KEY=generate-a-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

DB_ENGINE=django.db.backends.postgresql
DB_NAME=ddp_database
DB_USER=ddp_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

To generate a new SECRET_KEY:
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 5: Django Setup

```bash
cd myproject

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Create uploads directory
mkdir -p uploads
```

### Step 6: Setup Gunicorn Service

Create systemd service file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add this content (replace paths and username):
```ini
[Unit]
Description=Gunicorn daemon for Django DDP App
After=network.target

[Service]
User=your-username
Group=www-data
WorkingDirectory=/home/your-username/ddp-app/myproject
Environment="PATH=/home/your-username/ddp-app/venv/bin"
ExecStart=/home/your-username/ddp-app/venv/bin/gunicorn --config /home/your-username/ddp-app/gunicorn_config.py myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the service:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### Step 7: Configure Nginx

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/ddp

# Edit the config with your actual paths and domain
sudo nano /etc/nginx/sites-available/ddp
```

Update these in the nginx config:
- Replace `your-domain.com` with your actual domain
- Replace `/home/username/` with your actual path

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/ddp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

### Step 9: Setup SSL with Let's Encrypt (Recommended)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

After SSL setup, update your `.env`:
```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Then restart Gunicorn:
```bash
sudo systemctl restart gunicorn
```

---

## Post-Deployment

### Test Your Application

Visit your domain or server IP in a browser:
- Main site: `http://your-domain.com`
- Admin panel: `http://your-domain.com/admin`

### Common Commands

```bash
# Restart Gunicorn
sudo systemctl restart gunicorn

# Restart Nginx
sudo systemctl restart nginx

# View Gunicorn logs
sudo journalctl -u gunicorn -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Activate virtual environment
source /home/$USER/ddp-app/venv/bin/activate

# Run migrations
cd /home/$USER/ddp-app/myproject
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

### Updating the Application

```bash
# SSH into server
ssh username@your-server-ip

# Navigate to project
cd /home/$USER/ddp-app

# Activate virtual environment
source venv/bin/activate

# Pull latest changes (if using git)
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
cd myproject
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart gunicorn
```

---

## Troubleshooting

### Application not loading
1. Check Gunicorn status: `sudo systemctl status gunicorn`
2. Check logs: `sudo journalctl -u gunicorn -f`
3. Verify `.env` file configuration

### Static files not loading
1. Run: `python manage.py collectstatic --noinput`
2. Check nginx configuration for static files path
3. Verify permissions: `ls -la staticfiles/`

### Database connection errors
1. Verify PostgreSQL is running: `sudo systemctl status postgresql`
2. Check database credentials in `.env` file
3. Test connection: `sudo -u postgres psql -d ddp_database`

### 502 Bad Gateway
1. Check if Gunicorn is running: `sudo systemctl status gunicorn`
2. Verify the socket/port connection in nginx config
3. Check Gunicorn logs: `sudo journalctl -u gunicorn -f`

### Permission denied errors
```bash
# Fix uploads directory permissions
sudo chown -R $USER:www-data /home/$USER/ddp-app/myproject/uploads
sudo chmod -R 775 /home/$USER/ddp-app/myproject/uploads
```

---

## Security Checklist

- [ ] Changed SECRET_KEY from default
- [ ] Set DEBUG=False in production
- [ ] Configured ALLOWED_HOSTS properly
- [ ] Setup SSL certificate (HTTPS)
- [ ] Configured firewall (UFW)
- [ ] Using strong database password
- [ ] Regular backups configured
- [ ] Updated EMAIL credentials
- [ ] Removed default Django files (if any)
- [ ] Setup monitoring (optional)

---

## Backup Strategy

### Database Backup
```bash
# Create backup
pg_dump -U ddp_user ddp_database > backup_$(date +%Y%m%d).sql

# Restore backup
psql -U ddp_user ddp_database < backup_20260119.sql
```

### Files Backup
```bash
# Backup uploads directory
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz /home/$USER/ddp-app/myproject/uploads/
```

---

## Additional Resources

- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Gunicorn Documentation: https://docs.gunicorn.org/
- Nginx Documentation: https://nginx.org/en/docs/
- Let's Encrypt: https://letsencrypt.org/getting-started/

---

## Support

For issues specific to this application, refer to the project repository or contact the development team.
