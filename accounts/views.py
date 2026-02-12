from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from movies.models import Booking, Movie, SeatReservation
from datetime import datetime, timedelta

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to BookMyShow!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Login successful! Welcome back, {user.username}!')
            
            # Redirect to 'next' parameter if present, otherwise to profile
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    
    # Get user bookings
    all_bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    
    # Filter bookings
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'upcoming':
        bookings = all_bookings.filter(theater__time__gte=timezone.now())
    elif filter_type == 'past':
        bookings = all_bookings.filter(theater__time__lt=timezone.now())
    elif filter_type == 'completed':
        bookings = all_bookings.filter(payment_status='completed')
    else:
        bookings = all_bookings
    
    # Statistics
    total_bookings = all_bookings.filter(payment_status='completed').count()
    total_spent = all_bookings.filter(payment_status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    upcoming_bookings = all_bookings.filter(
        theater__time__gte=timezone.now(),
        payment_status='completed'
    ).count()
    
    # Favorite genres
    favorite_genres = Movie.objects.filter(
        bookings__user=request.user,
        bookings__payment_status='completed'
    ).values('genre').annotate(
        count=Count('bookings')
    ).exclude(genre__isnull=True).exclude(genre='').order_by('-count')[:5]
    
    # Recent activity (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_bookings_count = all_bookings.filter(
        booked_at__gte=thirty_days_ago,
        payment_status='completed'
    ).count()
    
    # Active reservations
    active_reservations = SeatReservation.objects.filter(
        user=request.user,
        is_active=True
    ).count()
    
    return render(request, 'profile.html', {
        'u_form': u_form,
        'bookings': bookings,
        'all_bookings': all_bookings,
        'total_bookings': total_bookings,
        'total_spent': total_spent,
        'upcoming_bookings': upcoming_bookings,
        'favorite_genres': favorite_genres,
        'recent_bookings_count': recent_bookings_count,
        'active_reservations': active_reservations,
        'filter_type': filter_type,
        'now': timezone.now(),
    })

@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'reset_password.html', {'form': form})