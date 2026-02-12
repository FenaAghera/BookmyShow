from django.core.management.base import BaseCommand
from movies.models import Theater, seat

class Command(BaseCommand):
    help = 'Add missing seats to all theaters that don\'t have 50 seats'

    def handle(self, *args, **options):
        theaters = Theater.objects.all()
        total_seats_added = 0
        theaters_fixed = 0
        
        for theater in theaters:
            existing_seats_count = seat.objects.filter(theater=theater).count()
            
            if existing_seats_count < 50:
                # Calculate how many seats to add
                seats_to_add = 50 - existing_seats_count
                
                # Get existing seat numbers to avoid duplicates
                existing_seat_numbers = set(seat.objects.filter(theater=theater).values_list('seat_number', flat=True))
                
                # Create seats (5 rows x 10 seats = 50 seats)
                seats_created = 0
                for row in ['A', 'B', 'C', 'D', 'E']:
                    for num in range(1, 11):
                        seat_number = f"{row}{num}"
                        if seat_number not in existing_seat_numbers:
                            seat.objects.create(
                                theater=theater,
                                seat_number=seat_number,
                                time=theater.time
                            )
                            existing_seat_numbers.add(seat_number)
                            seats_created += 1
                            total_seats_added += 1
                            
                            if seats_created >= seats_to_add:
                                break
                    if seats_created >= seats_to_add:
                        break
                
                theaters_fixed += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Fixed {theater.name} ({theater.movie.name}): Added {seats_created} seats (now has {seat.objects.filter(theater=theater).count()} seats)'
                    )
                )
            else:
                self.stdout.write(f'Skipping {theater.name} - already has {existing_seats_count} seats')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n[SUCCESS] Fixed {theaters_fixed} theaters, added {total_seats_added} seats total!'
            )
        )
