#!/bin/bash
# =========================================
# FOOTOP — Production Setup Script (cPanel)
# Run once after uploading to hosting
# =========================================

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Applying migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Done! Restart your app from cPanel Python App manager."
