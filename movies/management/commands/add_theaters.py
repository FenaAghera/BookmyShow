from django.core.management.base import BaseCommand
from movies.models import Movie, Theater, seat
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Add sample theaters and seats for ALL movies'

    def handle(self, *args, **options):
        movies = Movie.objects.all()
        
        if not movies.exists():
            self.stdout.write(self.style.WARNING('No movies found. Please run: python manage.py seed_movies'))
            return
        
        theater_names = ["PVR Cinemas", "INOX Theater", "Cinepolis", "Miraj Cinemas", "Carnival Cinemas"]
        
        total_theaters = 0
        total_seats = 0
        
        for movie in movies:
            # Check if movie already has theaters
            existing_theaters = Theater.objects.filter(movie=movie)
            if existing_theaters.exists():
                self.stdout.write(f'Skipping {movie.name} - already has {existing_theaters.count()} theaters')
                continue
            
            # Add 3-4 theaters for each movie with different showtimes
            theaters_to_create = []
            base_time = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
            
            # Add theaters with different showtimes throughout the day
            show_times = [
                base_time + timedelta(hours=2),   # 12:00 PM
                base_time + timedelta(hours=5),   # 3:00 PM
                base_time + timedelta(hours=8),  # 6:00 PM
                base_time + timedelta(hours=11), # 9:00 PM
            ]
            
            for i, show_time in enumerate(show_times):
                if i < len(theater_names):
                    theater_name = theater_names[i]
                else:
                    theater_name = f"Theater {i+1}"
                
                theater = Theater.objects.create(
                    name=theater_name,
                    movie=movie,
                    time=show_time
                )
                theaters_to_create.append(theater)
                total_theaters += 1
            
            # Create seats for each theater (5 rows x 10 seats = 50 seats per theater)
            for theater in theaters_to_create:
                for row in ['A', 'B', 'C', 'D', 'E']:
                    for num in range(1, 11):
                        seat.objects.create(
                            theater=theater,
                            seat_number=f"{row}{num}",
                            time=theater.time
                        )
                        total_seats += 1
            
            self.stdout.write(self.style.SUCCESS(f'Added {len(theaters_to_create)} theaters for {movie.name}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n[SUCCESS] Total: {total_theaters} theaters and {total_seats} seats created for {movies.count()} movies!'
        ))
