# 🔧 Fix Railway Crash - Set Environment Variables

## ❌ Problem

App is crashing because **missing environment variables**.

## ✅ Solution: Add These Variables to Railway

### Step 1: Go to Railway Dashboard

1. Go to **https://railway.app**
2. Click on your **project**
3. Click on **"web"** service
4. Click **"Variables"** tab

### Step 2: Add Required Variables

Click **"+ New Variable"** and add these **one by one**:

#### Variable 1: DJANGO_SECRET_KEY

**Name:** `DJANGO_SECRET_KEY`

**Value:** Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste as value.

#### Variable 2: DEBUG

**Name:** `DEBUG`

**Value:** `False`

#### Variable 3: ALLOWED_HOSTS

**Name:** `ALLOWED_HOSTS`

**Value:** `*.railway.app`

---

## 📋 Complete Variable List

Add these to Railway → Variables tab:

```
DJANGO_SECRET_KEY=<paste-generated-key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

**Note:** Railway automatically sets `DATABASE_URL` when you add PostgreSQL database.

---

## 🔍 Verify Database is Added

1. Go to Railway dashboard
2. Check if **PostgreSQL** database is added
3. If not:
   - Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
   - Railway auto-sets `DATABASE_URL` variable

---

## 🚀 After Adding Variables

1. **Redeploy** your service:
   - Click **"Deployments"** tab
   - Click **three dots** (⋯) on latest deployment
   - Click **"Redeploy"**

2. **Wait for deployment** (2-3 minutes)

3. **Check logs** - should see Django starting successfully

4. **Test URL** - should work now!

---

## ✅ Quick Checklist

- [ ] PostgreSQL database added to project
- [ ] `DJANGO_SECRET_KEY` variable added
- [ ] `DEBUG=False` variable added
- [ ] `ALLOWED_HOSTS=*.railway.app` variable added
- [ ] Service redeployed
- [ ] Status shows "Online"

---

## 🎯 Generate Secret Key

Run this locally to generate secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as `DJANGO_SECRET_KEY` value.

---

**Add these variables to Railway and redeploy - that should fix the crash!** 🚀
