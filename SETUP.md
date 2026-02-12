# BookMyShow - Setup Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## Configuration

### Email Configuration (for booking confirmations)

In `BookmyShow/settings.py`, configure email settings or set environment variables:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password for Gmail
DEFAULT_FROM_EMAIL = 'noreply@bookmyshow.com'
```

For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use that App Password in EMAIL_HOST_PASSWORD

### Razorpay Payment Gateway Configuration

**Note:** If Razorpay keys are not configured, the system will run in TEST MODE, allowing bookings without actual payment. This is useful for development and testing.

To enable real payments:

1. Sign up at https://razorpay.com
2. Get your Key ID and Key Secret from the dashboard
3. Set environment variables or update settings.py:

```python
RAZORPAY_KEY_ID = 'rzp_test_xxxxxxxxxxxxx'  # Your actual test key
RAZORPAY_KEY_SECRET = 'your_actual_razorpay_secret_key'  # Your actual secret
```

**For Testing Without Razorpay:**
- The system automatically detects missing/invalid keys
- Bookings will be confirmed without payment (TEST MODE)
- Perfect for development and testing

For production, use live keys from Razorpay dashboard.

## Features Implemented

✅ **Ticket Email Confirmation**
- Sends confirmation email after successful payment
- Includes: movie name, date, time, seat details, total amount, booking ID

✅ **Movie Trailers**
- Add YouTube trailer URL in Movie model (admin or via migration)
- Responsive embedded player on movie detail page

✅ **Payment Gateway Integration (Razorpay)**
- Integrated Razorpay for payment processing
- Handles payment success and failure cases
- Only confirms booking after successful payment

✅ **Responsive Design**
- Fully responsive for mobile, tablet, and desktop
- Bootstrap 4 with custom responsive styles

## Deployment Note

**Important**: Django applications cannot be deployed directly on Netlify or Vercel (they are for static sites and serverless functions).

For Django deployment, consider:
- **Railway** (https://railway.app) - Easy Django deployment
- **Render** (https://render.com) - Free tier available
- **Heroku** - Popular option
- **DigitalOcean App Platform**
- **AWS Elastic Beanstalk**

For static frontend + Django backend:
- Deploy Django API on Railway/Render
- Deploy frontend (if separated) on Netlify/Vercel

## Running the Project

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Adding Movies with Trailers

1. Go to Django admin: http://127.0.0.1:8000/admin/
2. Add a Movie
3. In the "Trailer URL" field, paste a YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
4. Save

The trailer will automatically appear on the movie detail page.
