# 🔧 Fix Railway Application Crash

## ❌ Error in Logs

```
Shutting down: Master
Worker exiting
```

This means your Django app is **crashing on startup**.

---

## 🔍 Common Causes & Fixes

### Cause 1: Missing ALLOWED_HOSTS

**Error:** Django rejects connections

**Fix:**
1. Go to Railway → Your service → **Variables** tab
2. Add:
   ```
   ALLOWED_HOSTS=*.railway.app
   ```
3. Redeploy

### Cause 2: Missing SECRET_KEY

**Error:** Django can't start without secret key

**Fix:**
1. Generate secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Add to Railway Variables:
   ```
   DJANGO_SECRET_KEY=<paste-generated-key>
   ```
3. Redeploy

### Cause 3: Database Connection Error

**Error:** Can't connect to database

**Fix:**
1. Make sure PostgreSQL database is added
2. Railway auto-sets database variables
3. Check Variables tab for:
   - `DATABASE_URL` (auto-set by Railway)
   - Or individual: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`

### Cause 4: Missing Dependencies

**Error:** Module not found

**Fix:**
- Railway installs from `requirements.txt` automatically
- Check if all packages are in requirements.txt

### Cause 5: Import Errors

**Error:** Can't import modules

**Fix:**
- Check for circular imports
- Verify all apps are in INSTALLED_APPS

---

## ✅ Required Environment Variables

Add these to Railway → Variables tab:

```
DJANGO_SECRET_KEY=<generate-random-key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

**Database variables are auto-set by Railway** (if PostgreSQL is added)

---

## 🔧 Step-by-Step Fix

### Step 1: Check Current Variables

1. Go to Railway dashboard
2. Click "web" service
3. Click **"Variables"** tab
4. Check what's there

### Step 2: Add Missing Variables

**Generate Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Add to Railway Variables:**
```
DJANGO_SECRET_KEY=<paste-generated-key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

### Step 3: Verify Database

1. Make sure PostgreSQL database is added to project
2. Railway automatically sets database variables
3. Check Variables tab for `DATABASE_URL`

### Step 4: Update Settings for Railway

Railway uses `DATABASE_URL` automatically. Let's make sure settings handle it:

---

## 📝 Update Settings for Railway

Railway provides database via `DATABASE_URL`. Let's update settings to use it:
