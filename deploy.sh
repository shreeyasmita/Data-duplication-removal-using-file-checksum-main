#!/bin/bash

# Django Data Deduplication Project - VPS Deployment Script
# This script automates the deployment process on Ubuntu/Debian VPS

set -e  # Exit on any error

echo "=========================================="
echo "Django DDP Deployment Script"
echo "=========================================="

# Update system packages
echo "Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
echo "Step 2: Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib

# Create project directory
echo "Step 3: Setting up project directory..."
PROJECT_DIR="/home/$USER/ddp-app"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Create and activate virtual environment
echo "Step 4: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Step 5: Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup PostgreSQL database
echo "Step 6: Setting up PostgreSQL database..."
echo "Please enter PostgreSQL password for user 'ddp_user' (remember this for .env file):"
read -s DB_PASSWORD

sudo -u postgres psql <<EOF
CREATE DATABASE ddp_database;
CREATE USER ddp_user WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE ddp_user SET client_encoding TO 'utf8';
ALTER ROLE ddp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ddp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ddp_database TO ddp_user;
\q
EOF

# Create .env file
echo "Step 7: Creating .env file..."
cat > $PROJECT_DIR/.env <<EOF
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

DB_ENGINE=django.db.backends.postgresql
DB_NAME=ddp_database
DB_USER=ddp_user
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF

echo "⚠️  IMPORTANT: Edit the .env file and update:"
echo "   - ALLOWED_HOSTS (add your domain/IP)"
echo "   - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD"

# Run Django migrations
echo "Step 8: Running database migrations..."
cd myproject
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Step 9: Collecting static files..."
python manage.py collectstatic --noinput

# Create Django superuser
echo "Step 10: Creating Django superuser..."
python manage.py createsuperuser

# Setup Gunicorn systemd service
echo "Step 11: Setting up Gunicorn service..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=Gunicorn daemon for Django DDP App
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR/myproject
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config $PROJECT_DIR/gunicorn_config.py myproject.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Start and enable Gunicorn service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Setup Nginx
echo "Step 12: Configuring Nginx..."
sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/ddp
sudo sed -i "s|/home/username|$PROJECT_DIR|g" /etc/nginx/sites-available/ddp
sudo ln -sf /etc/nginx/sites-available/ddp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Create uploads directory
echo "Step 13: Creating uploads directory..."
mkdir -p $PROJECT_DIR/myproject/uploads
sudo chown -R $USER:www-data $PROJECT_DIR/myproject/uploads
sudo chmod -R 775 $PROJECT_DIR/myproject/uploads

echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit $PROJECT_DIR/.env file with your actual configuration"
echo "2. Update nginx config: sudo nano /etc/nginx/sites-available/ddp"
echo "   - Replace 'your-domain.com' with your actual domain"
echo "3. Restart services:"
echo "   sudo systemctl restart gunicorn"
echo "   sudo systemctl restart nginx"
echo "4. Setup SSL with Let's Encrypt (optional but recommended):"
echo "   sudo apt install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d your-domain.com -d www.your-domain.com"
echo ""
echo "Your application should now be accessible at http://your-server-ip"
echo "=========================================="
