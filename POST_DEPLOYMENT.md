# 🎉 Post-Deployment Setup Guide

## ✅ Deployment Successful!

Your Django app is now live! Follow these steps to complete the setup.

---

## 📋 Step-by-Step Post-Deployment Tasks

### Step 1: Access Your Platform Console

**Railway:**
- Go to your project dashboard
- Click on your service
- Click **"View Logs"** or **"Shell"** tab

**Render:**
- Go to your dashboard
- Click on your web service
- Click **"Shell"** tab

---

### Step 2: Run Database Migrations

This sets up your database tables:

```bash
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, movies, accounts
Running migrations:
  Applying migrations... OK
```

---

### Step 3: Create Superuser (Admin Account)

This lets you access the admin panel:

```bash
python manage.py createsuperuser
```

**Follow prompts:**
- Username: (enter your username)
- Email: (enter your email)
- Password: (enter a strong password)
- Password (again): (confirm password)

**✅ Admin URL:** `https://your-app-url.com/admin/`

---

### Step 4: Seed Movies Data

Add sample movies with images and details:

```bash
python manage.py seed_movies
```

**Expected output:**
```
Downloading image for Avengers: Endgame...
[OK] Image saved for Avengers: Endgame
...
[SUCCESS] Seed complete. Created: X, Updated: Y
```

---

### Step 5: Add Theaters and Seats

Create theaters and seats for all movies:

```bash
python manage.py add_theaters
```

**Expected output:**
```
Added 4 theaters for Avengers: Endgame
Added 4 theaters for Avengers: Infinity War
...
[SUCCESS] Total: 68 theaters and 3400 seats created!
```

---

### Step 6: Collect Static Files

This gathers all CSS, JS, and images:

```bash
python manage.py collectstatic --noinput
```

**Expected output:**
```
Copying files...
...
X static files copied.
```

---

### Step 7: Verify Everything Works

Visit your live URL and test:

1. **Homepage**: `https://your-app-url.com/`
   - Should show movie list
   - Search and filters should work

2. **Register/Login**: `https://your-app-url.com/accounts/register/`
   - Create a test account
   - Login should work

3. **Movie Details**: Click any movie
   - Should show movie details
   - Trailer should play (if URL is set)
   - "Book Tickets" button should work

4. **Booking Flow**:
   - Select theater
   - Select seats
   - Proceed to payment
   - Complete booking (test mode works without payment)

5. **Profile**: `https://your-app-url.com/accounts/profile/`
   - Should show your bookings
   - Statistics should display

6. **Admin Dashboard**: `https://your-app-url.com/admin/`
   - Login with superuser credentials
   - Should see all models

7. **Admin Analytics**: `https://your-app-url.com/movies/admin/dashboard/`
   - Login as staff user
   - Should see analytics dashboard

---

## 🔧 Optional: Configure Environment Variables

### Email Configuration (For Booking Confirmations)

**Railway:**
- Go to project → Variables tab
- Add:
  ```
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_HOST_USER=your-email@gmail.com
  EMAIL_HOST_PASSWORD=your-app-password
  DEFAULT_FROM_EMAIL=noreply@bookmyshow.com
  ```

**Render:**
- Go to service → Environment tab
- Add same variables

**Note:** For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate App Password
3. Use App Password (not regular password)

### Razorpay Configuration (For Real Payments)

**Railway/Render:**
Add to environment variables:
```
RAZORPAY_KEY_ID=your-actual-key-id
RAZORPAY_KEY_SECRET=your-actual-secret-key
```

**Note:** Test mode works without Razorpay keys - bookings will be confirmed automatically.

---

## 🎯 Quick Setup Script

Run all setup commands at once:

```bash
# 1. Migrations
python manage.py migrate

# 2. Create superuser (interactive)
python manage.py createsuperuser

# 3. Seed data
python manage.py seed_movies
python manage.py add_theaters

# 4. Static files
python manage.py collectstatic --noinput

# 5. Verify
python manage.py check
```

---

## ✅ Post-Deployment Checklist

- [ ] Database migrations run successfully
- [ ] Superuser created
- [ ] Movies seeded (18 movies with images)
- [ ] Theaters and seats created
- [ ] Static files collected
- [ ] Homepage loads correctly
- [ ] User registration works
- [ ] Login works
- [ ] Movie browsing works
- [ ] Seat selection works
- [ ] Booking flow works
- [ ] Profile page displays bookings
- [ ] Admin panel accessible
- [ ] Admin dashboard accessible (if staff user)

---

## 🐛 Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Dependencies not installed
```bash
pip install -r requirements.txt
```

### Issue: "Table doesn't exist"
**Solution:** Run migrations
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution:** Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: "ALLOWED_HOSTS" error
**Solution:** Add your domain to environment variables
```
ALLOWED_HOSTS=your-app.railway.app,yourdomain.com
```

### Issue: Database connection error
**Solution:** Check database environment variables are set correctly

### Issue: Admin dashboard not accessible
**Solution:** Make sure user has `is_staff=True`
- Go to admin panel → Users
- Edit your user
- Check "Staff status"
- Save

---

## 📊 Verify Deployment

### Test These Features:

1. **User Features:**
   - ✅ Register new account
   - ✅ Login/Logout
   - ✅ Browse movies
   - ✅ Search movies
   - ✅ Filter by genre/language
   - ✅ View movie details
   - ✅ Watch trailers
   - ✅ Select seats
   - ✅ Complete booking
   - ✅ View profile
   - ✅ See booking history

2. **Admin Features:**
   - ✅ Access admin panel
   - ✅ View analytics dashboard
   - ✅ See revenue statistics
   - ✅ View popular movies
   - ✅ Manage bookings

3. **Technical:**
   - ✅ HTTPS enabled
   - ✅ Static files loading
   - ✅ Database working
   - ✅ Email sending (if configured)
   - ✅ Payment integration (test mode)

---

## 🎉 Success Indicators

Your deployment is successful when:

- ✅ Website loads without errors
- ✅ All pages accessible
- ✅ Database operations work
- ✅ User can register and login
- ✅ Booking flow completes
- ✅ Admin panel accessible
- ✅ No errors in logs

---

## 📝 Next Steps

1. **Share Your Live URL** for evaluation
2. **Test All Features** thoroughly
3. **Monitor Logs** for any errors
4. **Set Up Email** (optional but recommended)
5. **Configure Razorpay** (optional - for real payments)

---

## 🔗 Important URLs

- **Homepage**: `https://your-app-url.com/`
- **Admin Panel**: `https://your-app-url.com/admin/`
- **Admin Dashboard**: `https://your-app-url.com/movies/admin/dashboard/`
- **Profile**: `https://your-app-url.com/accounts/profile/`

---

## 📚 Additional Resources

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Django Docs: https://docs.djangoproject.com

---

**🎊 Congratulations! Your Django app is live and ready!**

Share your live URL and start testing! 🚀
