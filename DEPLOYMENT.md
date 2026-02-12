# Deployment Guide - BookMyShow Django Project

## ⚠️ Important: Netlify Limitation

**Django applications CANNOT be deployed directly on Netlify.**

Netlify is designed for:
- Static websites (HTML, CSS, JavaScript)
- Serverless functions (limited runtime)
- JAMstack applications

Django requires:
- Full Python runtime environment
- Persistent database (PostgreSQL, MySQL, etc.)
- WSGI/ASGI server
- Background tasks support

## ✅ Recommended Deployment Platforms for Django

### 1. **Railway** (Recommended - Easiest)
- **URL**: https://railway.app
- **Why**: Simplest Django deployment, automatic setup
- **Free Tier**: Yes (with limits)
- **Steps**:
  1. Sign up at Railway
  2. Connect GitHub repository
  3. Select Django template
  4. Railway auto-detects Django and sets up
  5. Add PostgreSQL database
  6. Set environment variables
  7. Deploy!

### 2. **Render** (Great Free Tier)
- **URL**: https://render.com
- **Why**: Generous free tier, easy setup
- **Free Tier**: Yes (spins down after inactivity)
- **Steps**:
  1. Sign up at Render
  2. Create new Web Service
  3. Connect GitHub repo
  4. Use build command: `pip install -r requirements.txt && python manage.py migrate`
  5. Start command: `gunicorn BookmyShow.wsgi:application`
  6. Add PostgreSQL database
  7. Deploy!

### 3. **Heroku** (Popular Choice)
- **URL**: https://heroku.com
- **Why**: Well-documented, reliable
- **Free Tier**: Discontinued (paid only)
- **Steps**:
  1. Install Heroku CLI
  2. Create `Procfile`: `web: gunicorn BookmyShow.wsgi:application`
  3. Create `runtime.txt`: `python-3.11.0`
  4. Deploy: `git push heroku main`

### 4. **DigitalOcean App Platform**
- **URL**: https://www.digitalocean.com/products/app-platform
- **Why**: Good performance, reasonable pricing
- **Free Tier**: No (but affordable)

### 5. **AWS Elastic Beanstalk**
- **URL**: https://aws.amazon.com/elasticbeanstalk/
- **Why**: Enterprise-grade, scalable
- **Free Tier**: Limited (12 months)

## 📋 Pre-Deployment Checklist

### 1. Update Settings for Production

Create `BookmyShow/settings_production.py`:

```python
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'your-app.railway.app']  # Add your domain

# Database (use PostgreSQL in production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files (use cloud storage in production)
# Consider AWS S3, Cloudinary, etc.

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Email (use real SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Razorpay (use real keys)
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
```

### 2. Update Requirements

Ensure `requirements.txt` includes production dependencies:

```txt
Django>=4.2,<5.0
razorpay>=1.4.0
Pillow>=10.0.0
requests>=2.31.0
gunicorn>=21.2.0
psycopg2-binary>=2.9.0
whitenoise>=6.5.0
```

### 3. Create Procfile (for Heroku/Railway)

Create `Procfile` in root directory:

```
web: gunicorn BookmyShow.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

### 4. Create Runtime File

Create `runtime.txt`:

```
python-3.11.0
```

### 5. Update WSGI Configuration

Ensure `BookmyShow/wsgi.py` is configured:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookmyShow.settings')

application = get_wsgi_application()
```

### 6. Static Files Configuration

Add to `settings.py`:

```python
# Static files (for production)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# WhiteNoise for static files (add to MIDDLEWARE)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 7. Environment Variables

Set these in your deployment platform:

```
DJANGO_SETCRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
```

## 🚀 Quick Deployment Steps (Railway)

1. **Prepare Repository**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Django
   - Add PostgreSQL database
   - Set environment variables
   - Deploy!

3. **Run Migrations**:
   Railway will automatically run migrations, or run manually:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

4. **Seed Data** (Optional):
   ```bash
   python manage.py seed_movies
   python manage.py add_theaters
   ```

## 📝 Post-Deployment Tasks

1. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Set Up Cron Job** (for cleanup reservations):
   ```bash
   */5 * * * * python manage.py cleanup_reservations
   ```

4. **Configure Domain** (if using custom domain)

5. **Set Up SSL** (usually automatic on most platforms)

## 🔧 Troubleshooting

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Ensure WhiteNoise middleware is added

### Database Errors
- Check database connection settings
- Ensure migrations are run: `python manage.py migrate`
- Verify environment variables are set

### Media Files Not Working
- Use cloud storage (AWS S3, Cloudinary) for production
- Or configure media file serving properly

### Email Not Sending
- Verify SMTP settings
- Check environment variables
- Test with console backend first

## 📚 Additional Resources

- Django Deployment Checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Heroku Django Guide: https://devcenter.heroku.com/articles/django-app-configuration

## ⚡ Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Seed data
python manage.py seed_movies
python manage.py add_theaters

# Run server
python manage.py runserver
```

---

**Note**: For evaluation purposes, Railway or Render are recommended as they offer free tiers and are easiest to set up. The project is ready for deployment on any Django-compatible platform.
