from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Theater, seat, Booking, SeatReservation
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError, transaction
from django.db.models import Sum, Count, Q
from .utils import send_booking_confirmation_email
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json

try:
    import razorpay
    from razorpay import errors as razorpay_errors
    RAZORPAY_AVAILABLE = True
except ImportError:
    razorpay_errors = None
    RAZORPAY_AVAILABLE = False

def movie_list(request):
    search_query = request.GET.get('search', '').strip()
    selected_genre = request.GET.get('genre', '').strip()
    selected_language = request.GET.get('language', '').strip()

    movies = Movie.objects.all()

    if search_query:
        movies = movies.filter(name__icontains=search_query)
    if selected_genre:
        movies = movies.filter(genre=selected_genre)
    if selected_language:
        movies = movies.filter(language=selected_language)

    db_genres = (
        Movie.objects.exclude(genre__isnull=True)
        .exclude(genre__exact='')
        .values_list('genre', flat=True)
        .distinct()
        .order_by('genre')
    )
    db_languages = (
        Movie.objects.exclude(language__isnull=True)
        .exclude(language__exact='')
        .values_list('language', flat=True)
        .distinct()
        .order_by('language')
    )

    default_genres = ['Action', 'Comedy', 'Drama', 'Romance', 'Thriller', 'Horror', 'Sci-Fi', 'Animation']
    default_languages = ['Hindi', 'English', 'Tamil', 'Telugu', 'Kannada', 'Malayalam']

    genres = sorted(set(default_genres) | set(db_genres))
    languages = sorted(set(default_languages) | set(db_languages))

    return render(
        request,
        'movies/movie_list.html',
        {
            'movies': movies,
            'genres': genres,
            'languages': languages,
            'search_query': search_query,
            'selected_genre': selected_genre,
            'selected_language': selected_language,
        },
    )
    
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    trailer_embed_url = movie.get_trailer_embed_url()
    return render(request, 'movies/movie_detail.html', {
        'movie': movie, 
        'theaters': theaters,
        'trailer_embed_url': trailer_embed_url
    })

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

@login_required(login_url='/accounts/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    
    # Cleanup expired reservations
    SeatReservation.cleanup_expired()
    
    seats = seat.objects.filter(theater=theater).order_by('seat_number')
    
    # Check if theater has seats
    if not seats.exists():
        messages.error(request, 'This theater has no seats available. Please contact support.')
        return redirect('theater_list', movie_id=theater.movie.id)
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []
        if not selected_seats:
            return render(request, "movies/seat_selection.html",  {'theater': theater, 'seats': seats, 'error_message': 'No seats selected.'})
        
        # Check if seats are available (not booked and not reserved by others)
        seat_objects = []
        for seat_id in selected_seats:
            seat_obj = get_object_or_404(seat, id=seat_id, theater=theater)
            if seat_obj.is_booked:
                error_seats.append(f"{seat_obj.seat_number} (Booked)")
            elif seat_obj.is_reserved():
                reservation = seat_obj.get_reservation()
                if reservation and reservation.user != request.user:
                    error_seats.append(f"{seat_obj.seat_number} (Reserved by another user)")
                else:
                    seat_objects.append(seat_obj)
            else:
                seat_objects.append(seat_obj)
        
        if error_seats:
            error_message = f"The following seats are unavailable: {', '.join(error_seats)}"
            return render(request, "movies/seat_selection.html", {'theater': theater, 'seats': seats, 'error_message': error_message})
        
        # Create reservations for selected seats
        reservation_ids = []
        try:
            with transaction.atomic():
                for seat_obj in seat_objects:
                    # Release any existing reservation for this seat by this user
                    SeatReservation.objects.filter(
                        seat=seat_obj,
                        user=request.user,
                        is_active=True
                    ).update(is_active=False)
                    
                    # Create new reservation
                    reservation = SeatReservation.objects.create(
                        user=request.user,
                        seat=seat_obj,
                        theater=theater
                    )
                    reservation_ids.append(reservation.id)
        except IntegrityError:
            messages.error(request, 'Some seats became unavailable. Please try again.')
            return render(request, "movies/seat_selection.html", {'theater': theater, 'seats': seats})
        
        # Calculate total amount (₹200 per seat)
        seat_price = 200
        total_amount = len(seat_objects) * seat_price
        
        # Store selected seats and reservations in session for payment
        request.session['selected_seats'] = selected_seats
        request.session['reservation_ids'] = reservation_ids
        request.session['theater_id'] = theater_id
        request.session['total_amount'] = float(total_amount)
        request.session['seat_count'] = len(seat_objects)
        
        messages.info(request, 'Seats reserved for 5 minutes. Please complete payment to confirm your booking.')
        return redirect('initiate_payment')
    
    # For GET request, show seats with reservation status
    return render(request, 'movies/seat_selection.html', {'theater': theater, 'seats': seats})

@login_required(login_url='/accounts/login/')
def initiate_payment(request):
    if not RAZORPAY_AVAILABLE:
        messages.error(request, 'Payment gateway is not configured. Please install razorpay package.')
        return redirect('movie_list')
    
    if 'selected_seats' not in request.session:
        messages.error(request, 'No seats selected. Please select seats first.')
        return redirect('movie_list')
    
    theater_id = request.session.get('theater_id')
    total_amount = request.session.get('total_amount', 0)
    seat_count = request.session.get('seat_count', 0)
    
    theater = get_object_or_404(Theater, id=theater_id)
    
    # Check if reservations are still valid
    reservation_ids = request.session.get('reservation_ids', [])
    if reservation_ids:
        valid_reservations = SeatReservation.objects.filter(
            id__in=reservation_ids,
            user=request.user,
            is_active=True
        )
        expired_count = len(reservation_ids) - valid_reservations.count()
        if expired_count > 0:
            messages.warning(request, f'{expired_count} seat reservation(s) expired. Please select seats again.')
            return redirect('book_seats', theater_id=theater_id)
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create order
    amount_in_paise = int(total_amount * 100)  # Convert to paise
    order_data = {
        'amount': amount_in_paise,
        'currency': 'INR',
        'receipt': f'order_{theater_id}_{request.user.id}',
        'notes': {
            'theater_id': str(theater_id),
            'user_id': str(request.user.id),
        }
    }
    
    # Check if Razorpay keys are configured (not placeholder values)
    if (settings.RAZORPAY_KEY_ID == 'rzp_test_xxxxxxxxxxxxx' or 
        settings.RAZORPAY_KEY_SECRET == 'your_razorpay_secret_key' or
        'xxxxx' in settings.RAZORPAY_KEY_ID):
        # Test mode - allow booking without payment
        messages.warning(request, 'Payment gateway not configured. Proceeding in test mode (booking will be confirmed without payment).')
        
        # Directly create booking without payment
        selected_seats = request.session.get('selected_seats', [])
        reservation_ids = request.session.get('reservation_ids', [])
        
        if not selected_seats:
            messages.error(request, 'No seats selected.')
            return redirect('book_seats', theater_id=theater_id)
        
        bookings = []
        with transaction.atomic():
            # Confirm reservations
            if reservation_ids:
                SeatReservation.objects.filter(
                    id__in=reservation_ids,
                    user=request.user,
                    is_active=True
                ).update(confirmed=True, is_active=False)
            
            for seat_id in selected_seats:
                seat_obj = get_object_or_404(seat, id=seat_id, theater=theater)
                if seat_obj.is_booked:
                    continue
                
                SeatReservation.objects.filter(
                    seat=seat_obj,
                    is_active=True
                ).update(is_active=False)
                
                try:
                    booking = Booking.objects.create(
                        user=request.user,
                        seat=seat_obj,
                        movie=theater.movie,
                        theater=theater,
                        amount=total_amount / len(selected_seats),
                        payment_status='completed',
                        payment_id='TEST_MODE_NO_PAYMENT',
                        razorpay_order_id='TEST_MODE'
                    )
                    seat_obj.is_booked = True
                    seat_obj.save()
                    bookings.append(booking)
                except IntegrityError:
                    continue
        
        if bookings:
            for booking in bookings:
                send_booking_confirmation_email(booking)
            
            request.session.pop('selected_seats', None)
            request.session.pop('reservation_ids', None)
            request.session.pop('theater_id', None)
            request.session.pop('total_amount', None)
            request.session.pop('seat_count', None)
            
            messages.success(request, f'Booking confirmed! (Test Mode - No payment required). Confirmation email sent to {request.user.email}')
            return redirect('profile')
        else:
            messages.error(request, 'Failed to create bookings.')
            return redirect('book_seats', theater_id=theater_id)
    
    try:
        order = client.order.create(data=order_data)
        order_id = order['id']
        
        context = {
            'theater': theater,
            'total_amount': total_amount,
            'seat_count': seat_count,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order_id,
            'amount': amount_in_paise,
        }
        
        # Store order_id in session
        request.session['razorpay_order_id'] = order_id
        
        return render(request, 'movies/payment.html', context)
    except Exception as e:
        error_msg = str(e)
        if 'Authentication failed' in error_msg or 'authentication' in error_msg.lower() or 'Bad Request' in error_msg:
            # Razorpay keys are invalid - use test mode
            messages.warning(request, 'Payment gateway not configured. Proceeding in test mode (booking will be confirmed without payment).')
            
            # Directly create booking without payment
            selected_seats = request.session.get('selected_seats', [])
            reservation_ids = request.session.get('reservation_ids', [])
            
            if not selected_seats:
                messages.error(request, 'No seats selected.')
                return redirect('book_seats', theater_id=theater_id)
            
            bookings = []
            with transaction.atomic():
                # Confirm reservations
                if reservation_ids:
                    SeatReservation.objects.filter(
                        id__in=reservation_ids,
                        user=request.user,
                        is_active=True
                    ).update(confirmed=True, is_active=False)
                
                for seat_id in selected_seats:
                    seat_obj = get_object_or_404(seat, id=seat_id, theater=theater)
                    if seat_obj.is_booked:
                        continue
                    
                    SeatReservation.objects.filter(
                        seat=seat_obj,
                        is_active=True
                    ).update(is_active=False)
                    
                    try:
                        booking = Booking.objects.create(
                            user=request.user,
                            seat=seat_obj,
                            movie=theater.movie,
                            theater=theater,
                            amount=total_amount / len(selected_seats),
                            payment_status='completed',
                            payment_id='TEST_MODE_NO_PAYMENT',
                            razorpay_order_id='TEST_MODE'
                        )
                        seat_obj.is_booked = True
                        seat_obj.save()
                        bookings.append(booking)
                    except IntegrityError:
                        continue
            
            if bookings:
                for booking in bookings:
                    send_booking_confirmation_email(booking)
                
                request.session.pop('selected_seats', None)
                request.session.pop('reservation_ids', None)
                request.session.pop('theater_id', None)
                request.session.pop('total_amount', None)
                request.session.pop('seat_count', None)
                
                messages.success(request, f'Booking confirmed! (Test Mode - No payment required). Confirmation email sent to {request.user.email}')
                return redirect('profile')
            else:
                messages.error(request, 'Failed to create bookings.')
                return redirect('book_seats', theater_id=theater_id)
        else:
            messages.error(request, f'Payment initialization failed: {error_msg}')
            return redirect('book_seats', theater_id=theater_id)

@login_required(login_url='/accounts/login/')
def payment_success(request):
    if not RAZORPAY_AVAILABLE:
        messages.error(request, 'Payment gateway is not configured.')
        return redirect('movie_list')
    
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        # Verify payment signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            # Verify signature
            client.utility.verify_payment_signature(params_dict)
            
            # Payment verified, create bookings and confirm reservations
            theater_id = request.session.get('theater_id')
            selected_seats = request.session.get('selected_seats', [])
            reservation_ids = request.session.get('reservation_ids', [])
            total_amount = request.session.get('total_amount', 0)
            
            theater = get_object_or_404(Theater, id=theater_id)
            bookings = []
            
            with transaction.atomic():
                # Confirm reservations first
                if reservation_ids:
                    SeatReservation.objects.filter(
                        id__in=reservation_ids,
                        user=request.user,
                        is_active=True
                    ).update(confirmed=True, is_active=False)
                
                for seat_id in selected_seats:
                    seat_obj = get_object_or_404(seat, id=seat_id, theater=theater)
                    if seat_obj.is_booked:
                        continue
                    
                    # Release any active reservation for this seat
                    SeatReservation.objects.filter(
                        seat=seat_obj,
                        is_active=True
                    ).update(is_active=False)
                    
                    try:
                        booking = Booking.objects.create(
                            user=request.user,
                            seat=seat_obj,
                            movie=theater.movie,
                            theater=theater,
                            amount=total_amount / len(selected_seats),  # Amount per seat
                            payment_status='completed',
                            payment_id=razorpay_payment_id,
                            razorpay_order_id=razorpay_order_id
                        )
                        seat_obj.is_booked = True
                        seat_obj.save()
                        bookings.append(booking)
                    except IntegrityError:
                        continue
                
                if bookings:
                    # Send confirmation email for each booking
                    for booking in bookings:
                        send_booking_confirmation_email(booking)
                    
                    # Clear session
                    request.session.pop('selected_seats', None)
                    request.session.pop('reservation_ids', None)
                    request.session.pop('theater_id', None)
                    request.session.pop('total_amount', None)
                    request.session.pop('seat_count', None)
                    request.session.pop('razorpay_order_id', None)
                    
                    messages.success(request, f'Payment successful! Booking confirmed. Confirmation email sent to {request.user.email}')
                    return redirect('profile')
                else:
                    messages.error(request, 'Failed to create bookings. Please contact support.')
                    return redirect('movie_list')
                    
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, 'Payment verification failed. Please try again.')
            return redirect('initiate_payment')
        except Exception as e:
            messages.error(request, f'Payment processing error: {str(e)}')
            return redirect('initiate_payment')
    
    return redirect('movie_list')

@login_required(login_url='/accounts/login/')
def payment_failure(request):
    messages.error(request, 'Payment failed. Please try again or select different seats.')
    theater_id = request.session.get('theater_id')
    
    # Release reservations on payment failure
    reservation_ids = request.session.get('reservation_ids', [])
    if reservation_ids:
        SeatReservation.objects.filter(
            id__in=reservation_ids,
            user=request.user,
            is_active=True
        ).update(is_active=False)
    
    # Clear session
    request.session.pop('selected_seats', None)
    request.session.pop('reservation_ids', None)
    request.session.pop('theater_id', None)
    request.session.pop('total_amount', None)
    request.session.pop('seat_count', None)
    request.session.pop('razorpay_order_id', None)
    
    if theater_id:
        return redirect('book_seats', theater_id=theater_id)
    return redirect('movie_list')

# Admin Dashboard
def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/accounts/login/')
def admin_dashboard(request):
    # Cleanup expired reservations
    SeatReservation.cleanup_expired()
    
    # Total Revenue from completed bookings
    total_revenue = Booking.objects.filter(
        payment_status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Most Popular Movies (by number of tickets sold)
    popular_movies = Movie.objects.annotate(
        ticket_count=Count('bookings', filter=Q(bookings__payment_status='completed'))
    ).filter(ticket_count__gt=0).order_by('-ticket_count')[:10]
    
    # Busiest Theaters (by number of bookings)
    busy_theaters = Theater.objects.annotate(
        booking_count=Count('bookings', filter=Q(bookings__payment_status='completed'))
    ).filter(booking_count__gt=0).order_by('-booking_count')[:10]
    
    # Busiest Showtimes
    busy_showtimes = Theater.objects.annotate(
        booking_count=Count('bookings', filter=Q(bookings__payment_status='completed'))
    ).filter(booking_count__gt=0).order_by('-booking_count')[:10]
    
    # Recent Bookings
    recent_bookings = Booking.objects.filter(
        payment_status='completed'
    ).order_by('-booked_at')[:10]
    
    # Statistics
    total_bookings = Booking.objects.filter(payment_status='completed').count()
    total_movies = Movie.objects.count()
    total_theaters = Theater.objects.count()
    active_reservations = SeatReservation.objects.filter(is_active=True).count()
    
    # Revenue by Movie
    revenue_by_movie = Movie.objects.annotate(
        revenue=Sum('bookings__amount', filter=Q(bookings__payment_status='completed'))
    ).filter(revenue__gt=0).order_by('-revenue')[:10]
    
    context = {
        'total_revenue': total_revenue,
        'popular_movies': popular_movies,
        'busy_theaters': busy_theaters,
        'busy_showtimes': busy_showtimes,
        'recent_bookings': recent_bookings,
        'total_bookings': total_bookings,
        'total_movies': total_movies,
        'total_theaters': total_theaters,
        'active_reservations': active_reservations,
        'revenue_by_movie': revenue_by_movie,
    }
    
    return render(request, 'movies/admin_dashboard.html', context)
