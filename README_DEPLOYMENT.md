# 🚀 Quick Deployment Guide

## ⚠️ CRITICAL: Netlify Cannot Host Django

**Django applications CANNOT run on Netlify.** Netlify is for static sites only.

## ✅ Use These Platforms Instead:

### Option 1: Railway (Easiest - Recommended)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway auto-detects Django
6. Add PostgreSQL database
7. Set environment variables (see below)
8. Deploy!

**Free tier available!**

### Option 2: Render (Best Free Tier)
1. Go to https://render.com
2. Sign up with GitHub
3. Create "New Web Service"
4. Connect repository
5. Build: `pip install -r requirements.txt && python manage.py migrate`
6. Start: `gunicorn BookmyShow.wsgi:application`
7. Add PostgreSQL database
8. Set environment variables
9. Deploy!

**Free tier available!**

## 🔑 Required Environment Variables

Set these in your deployment platform:

```
DJANGO_SECRET_KEY=generate-a-long-random-string-here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,yourdomain.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=5432
```

Optional (for email):
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Optional (for payments):
```
RAZORPAY_KEY_ID=your-key
RAZORPAY_KEY_SECRET=your-secret
```

## 📝 After Deployment

Run these commands in your platform's console:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py seed_movies
python manage.py add_theaters
```

## ✅ Project Status

- ✅ No errors found
- ✅ All dependencies ready
- ✅ All migrations ready
- ✅ All movies have images
- ✅ Production settings template created
- ✅ Deployment files ready

**The project is 100% ready for deployment!**

For detailed instructions, see `DEPLOYMENT.md`.
