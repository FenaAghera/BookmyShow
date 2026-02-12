from django.contrib import admin
from .models import Movie, Theater, seat, Booking, SeatReservation

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'genre', 'language', 'cast', 'description']

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie','time']

@admin.register(seat)
class seatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number','is_booked']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user','seat','movie','theater','booked_at', 'payment_status', 'amount']
    list_filter = ['payment_status', 'booked_at']
    search_fields = ['booking_id', 'user__username', 'movie__name']

@admin.register(SeatReservation)
class SeatReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'theater', 'reserved_at', 'expires_at', 'is_active', 'confirmed']
    list_filter = ['is_active', 'confirmed', 'reserved_at']
    search_fields = ['user__username', 'seat__seat_number']
    readonly_fields = ['reserved_at', 'expires_at']
