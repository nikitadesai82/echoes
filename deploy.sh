#!/usr/bin/env bash
# Deploy latest GitHub main branch to this droplet.
# Usage: ssh root@146.190.149.8 then run: ./deploy.sh
set -e

cd /var/www/eon

echo "==> Pulling latest changes from GitHub..."
git pull origin main

echo "==> Activating virtual environment..."
source echo/bin/activate

cd eon

echo "==> Applying database migrations (no-op if none pending)..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Restarting gunicorn..."
sudo systemctl restart gunicorn

echo "==> Restarting nginx..."
sudo systemctl restart nginx

echo "==> Deploy complete."
