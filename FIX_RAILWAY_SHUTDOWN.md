# Fix Railway App Shutting Down After 5 Seconds

## Problem
The app starts successfully but shuts down after ~5 seconds. This is typically caused by:
1. **Health check failure** - Railway expects the app to respond to HTTP requests
2. **Missing environment variables** - SECRET_KEY, ALLOWED_HOSTS, DATABASE_URL
3. **Database connection errors** during startup

## Solutions Applied

### 1. Health Check Endpoint Added
- Added `/health/` endpoint that returns "OK" (200 status)
- Railway can now verify the app is running

### 2. Database Connection Fix
- Improved error handling for database connections
- Graceful fallback to SQLite if PostgreSQL isn't available during startup

## Next Steps

### 1. Verify Environment Variables on Railway
Go to your Railway project → **Variables** tab and ensure these are set:

**Required:**
- `SECRET_KEY` - Django secret key (generate one if missing)
- `ALLOWED_HOSTS` - Your Railway domain (e.g., `web-production-xxxxx.up.railway.app`)
- `DATABASE_URL` - Should be auto-set by Railway if you added a PostgreSQL service

**Optional (for email):**
- `EMAIL_HOST_USER` - Your email
- `EMAIL_HOST_PASSWORD` - Your email password

**Optional (for payment):**
- `RAZORPAY_KEY_ID` - Your Razorpay key
- `RAZORPAY_KEY_SECRET` - Your Razorpay secret

### 2. Check Railway Logs
1. Go to Railway dashboard → Your service → **Deployments** tab
2. Click on the latest deployment
3. Check **Logs** for any error messages

### 3. Verify Health Check
After deployment, test the health endpoint:
```
https://your-app-name.up.railway.app/health/
```
Should return: `OK`

### 4. Check Railway Health Check Settings
Railway might be checking the wrong path. The health check endpoint is now at `/health/`.

If Railway has custom health check settings, make sure they point to `/health/` or `/`.

## Common Issues

### Issue: "No directory at: /app/staticfiles/"
**Solution:** Already fixed - `os.makedirs(STATIC_ROOT, exist_ok=True)` was added to settings.py

### Issue: Database connection errors
**Solution:** The app now gracefully falls back to SQLite if PostgreSQL isn't available. However, you should still set `DATABASE_URL` properly.

### Issue: Missing SECRET_KEY
**Solution:** Generate one:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Then add it to Railway environment variables.

## Testing Locally
Test the health endpoint locally:
```bash
python manage.py runserver
# In another terminal:
curl http://localhost:8000/health/
# Should return: OK
```

## After Fix
Once the app stays online:
1. Run migrations: `railway run python manage.py migrate`
2. Create superuser: `railway run python manage.py createsuperuser`
3. Seed data: `railway run python manage.py seed_movies`
4. Add theaters: `railway run python manage.py add_theaters`
