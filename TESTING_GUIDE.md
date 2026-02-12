# Testing Guide - BookMyShow Project

## Server Status
The development server should be running at: **http://127.0.0.1:8000/**

## Step-by-Step Testing

### 1. **Access the Homepage**
- Open browser: http://127.0.0.1:8000/
- Should redirect to: http://127.0.0.1:8000/movies/
- ✅ **Expected**: See movie list page with search and filter options

### 2. **Test User Registration/Login**
- Click "Register" in navbar
- Create a new account
- ✅ **Expected**: Redirected to profile page after registration
- Logout and login again
- ✅ **Expected**: Successful login

### 3. **Test Movie List Features**
- Try searching for movies
- Filter by genre
- Filter by language
- ✅ **Expected**: Filters work correctly

### 4. **Test Movie Detail Page with Trailer**
- Click "View Details" on any movie
- ✅ **Expected**: 
  - Movie details displayed
  - If trailer URL is set, YouTube trailer should be embedded
  - Responsive on mobile/tablet/desktop
- Click "Book Tickets" button
- ✅ **Expected**: Redirects to theater list

### 5. **Test Theater Selection**
- Select a theater
- ✅ **Expected**: See theater list with show times
- Click "Book Seats"
- ✅ **Expected**: Redirects to seat selection page

### 6. **Test Seat Selection**
- Select one or more available seats
- ✅ **Expected**: 
  - Selected seats highlighted in green
  - Booked seats shown as unavailable
  - Responsive seat map
- Click "Proceed to Payment"
- ✅ **Expected**: Redirects to payment page

### 7. **Test Payment Integration (Razorpay)**
- On payment page, verify booking summary is correct
- Click "Pay ₹XXX" button
- ✅ **Expected**: 
  - Razorpay checkout popup opens
  - Can use test card: 4111 1111 1111 1111
  - CVV: Any 3 digits
  - Expiry: Any future date

**Test Payment Scenarios:**
- **Success**: Complete payment → Should redirect to profile with success message
- **Failure**: Close popup or fail payment → Should show error message

### 8. **Test Email Confirmation**
- After successful payment
- ✅ **Expected**: 
  - Booking confirmed message
  - Email sent to user's email address
  - Check email inbox for confirmation (if email configured)

### 9. **Test Profile Page**
- Go to Profile page
- ✅ **Expected**: 
  - See user bookings with:
    - Booking ID
    - Movie name
    - Theater name
    - Seat number
    - Show time
    - Amount paid
    - Payment status

### 10. **Test Responsive Design**
- Open browser DevTools (F12)
- Test on different screen sizes:
  - Mobile (375px)
  - Tablet (768px)
  - Desktop (1920px)
- ✅ **Expected**: All pages adapt properly to screen size

## Quick Test Checklist

- [ ] Server starts without errors
- [ ] Homepage loads
- [ ] User can register/login
- [ ] Movie list displays
- [ ] Movie detail page shows trailer (if URL set)
- [ ] Seat selection works
- [ ] Payment page loads
- [ ] Razorpay integration works (test mode)
- [ ] Booking confirmation appears
- [ ] Profile shows bookings
- [ ] Responsive on mobile/tablet/desktop

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'razorpay'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Payment not working
**Solution**: Check Razorpay keys in settings.py
- Use test keys for development
- Format: `rzp_test_xxxxxxxxxxxxx`

### Issue: Email not sending
**Solution**: 
- Check email settings in settings.py
- For Gmail: Use App Password (not regular password)
- For testing: Email backend is set to console (check terminal output)

### Issue: Trailer not showing
**Solution**: 
- Add trailer URL in Django admin
- Format: `https://www.youtube.com/watch?v=VIDEO_ID`
- Or: `https://youtu.be/VIDEO_ID`

## Test Data Setup

To test with sample data, run:
```bash
python manage.py seed_movies
python manage.py add_theaters
```

Then add trailer URLs in Django admin for movies.

## Admin Access

Create superuser:
```bash
python manage.py createsuperuser
```

Access admin: http://127.0.0.1:8000/admin/
- Add movies with trailer URLs
- View bookings
- Manage theaters
