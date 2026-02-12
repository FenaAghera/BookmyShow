#!/bin/bash
# Quick Setup Script for Post-Deployment

echo "🚀 Starting Post-Deployment Setup..."

# Step 1: Run Migrations
echo "📦 Running database migrations..."
python manage.py migrate

# Step 2: Collect Static Files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Step 3: Seed Movies
echo "🎬 Seeding movies..."
python manage.py seed_movies

# Step 4: Add Theaters
echo "🎭 Adding theaters and seats..."
python manage.py add_theaters

# Step 5: System Check
echo "✅ Running system check..."
python manage.py check

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Create superuser: python manage.py createsuperuser"
echo "2. Visit your live URL and test the app"
echo "3. Access admin: https://your-app-url.com/admin/"
echo ""
