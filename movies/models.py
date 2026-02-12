from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Movie(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True, help_text="YouTube trailer URL")

    def __str__(self):
        return self.name
    
    def get_trailer_embed_url(self):
        """Convert YouTube URL to embed format"""
        if not self.trailer_url:
            return None
        # Handle different YouTube URL formats
        if 'youtube.com/watch?v=' in self.trailer_url:
            video_id = self.trailer_url.split('v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtu.be/' in self.trailer_url:
            video_id = self.trailer_url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtube.com/embed/' in self.trailer_url:
            return self.trailer_url
        return None

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'
    
class seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)  
    is_booked = models.BooleanField(default=False)
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.seat_number} - {self.theater.name}'
    
    def is_reserved(self):
        """Check if seat is currently reserved (not expired)"""
        reservation = SeatReservation.objects.filter(
            seat=self,
            is_active=True
        ).first()
        if reservation:
            return reservation.is_valid()
        return False
    
    def get_reservation(self):
        """Get active reservation for this seat"""
        return SeatReservation.objects.filter(
            seat=self,
            is_active=True
        ).first()
    
class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    seat = models.OneToOneField(seat, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookings')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    booking_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            import uuid
            self.booking_id = f"BMS{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class SeatReservation(models.Model):
    """Temporary seat reservation (5 minutes timeout)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seat_reservations')
    seat = models.ForeignKey(seat, on_delete=models.CASCADE, related_name='reservations')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seat_reservations')
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)  # True when payment is completed
    
    class Meta:
        unique_together = ['seat', 'is_active']
        indexes = [
            models.Index(fields=['expires_at', 'is_active']),
        ]
    
    def __str__(self):
        return f'Reservation for {self.seat.seat_number} by {self.user.username}'
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set expiration to 5 minutes from now
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if reservation is still valid (not expired)"""
        if not self.is_active:
            return False
        return timezone.now() < self.expires_at
    
    def release(self):
        """Release the reservation"""
        self.is_active = False
        self.save()
    
    @staticmethod
    def cleanup_expired():
        """Remove expired reservations"""
        expired = SeatReservation.objects.filter(
            is_active=True,
            expires_at__lt=timezone.now(),
            confirmed=False
        )
        count = expired.count()
        expired.update(is_active=False)
        return count