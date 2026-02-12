from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_booking_confirmation_email(booking):
    """Send booking confirmation email to user"""
    subject = f'Booking Confirmation - {booking.movie.name}'
    
    context = {
        'user': booking.user,
        'booking': booking,
        'movie': booking.movie,
        'theater': booking.theater,
        'seat': booking.seat,
    }
    
    message = render_to_string('movies/booking_confirmation_email.html', context)
    
    send_mail(
        subject=subject,
        message='',
        html_message=message,
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bookmyshow.com',
        recipient_list=[booking.user.email],
        fail_silently=False,
    )