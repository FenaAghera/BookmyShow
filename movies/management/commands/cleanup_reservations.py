from django.core.management.base import BaseCommand
from movies.models import SeatReservation

class Command(BaseCommand):
    help = 'Clean up expired seat reservations'

    def handle(self, *args, **options):
        count = SeatReservation.cleanup_expired()
        self.stdout.write(
            self.style.SUCCESS(f'Cleaned up {count} expired reservations')
        )
