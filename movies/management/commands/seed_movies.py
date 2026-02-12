from django.core.management.base import BaseCommand
from movies.models import Movie
import requests
import os
from django.conf import settings
from urllib.parse import urlparse

class Command(BaseCommand):
    help = "Seed the database with sample movies with detailed information and images"

    def handle(self, *args, **options):
        # Movie data with detailed information
        movies_to_seed = [
            {
                "name": "Avengers: Endgame",
                "genre": "Action",
                "language": "English",
                "rating": "9.0",
                "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth, Scarlett Johansson, Jeremy Renner",
                "description": "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.",
                "trailer_url": "https://www.youtube.com/watch?v=TcMBFSGVi1c",
                "image_url": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg"
            },
            {
                "name": "Avengers: Infinity War",
                "genre": "Action",
                "language": "English",
                "rating": "8.8",
                "cast": "Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans, Scarlett Johansson, Josh Brolin",
                "description": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.",
                "trailer_url": "https://www.youtube.com/watch?v=6ZfuNTqbHE8",
                "image_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"
            },
            {
                "name": "Spider-Man: No Way Home",
                "genre": "Action",
                "language": "English",
                "rating": "8.4",
                "cast": "Tom Holland, Zendaya, Benedict Cumberbatch, Jacob Batalon, Willem Dafoe",
                "description": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.",
                "trailer_url": "https://www.youtube.com/watch?v=JfVOs4VSpmA",
                "image_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"
            },
            {
                "name": "The Dark Knight",
                "genre": "Action",
                "language": "English",
                "rating": "9.0",
                "cast": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine, Gary Oldman",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "trailer_url": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
                "image_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg"
            },
            {
                "name": "Inception",
                "genre": "Thriller",
                "language": "English",
                "rating": "8.8",
                "cast": "Leonardo DiCaprio, Marion Cotillard, Tom Hardy, Joseph Gordon-Levitt, Ellen Page",
                "description": "A skilled thief is given a chance at redemption if he can pull off an impossible task: Inception, the implantation of another person's idea into a target's subconscious.",
                "trailer_url": "https://www.youtube.com/watch?v=YoHD9XEInc0",
                "image_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg"
            },
            {
                "name": "Interstellar",
                "genre": "Sci-Fi",
                "language": "English",
                "rating": "8.7",
                "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine, Matt Damon",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival while Earth is becoming uninhabitable.",
                "trailer_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E",
                "image_url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg"
            },
            {
                "name": "Toy Story",
                "genre": "Animation",
                "language": "English",
                "rating": "8.3",
                "cast": "Tom Hanks, Tim Allen, Don Rickles, Jim Varney, Wallace Shawn",
                "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.",
                "trailer_url": "https://www.youtube.com/watch?v=v-PjgYDrg70",
                "image_url": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzY@._V1_.jpg"
            },
            {
                "name": "Coco",
                "genre": "Animation",
                "language": "English",
                "rating": "8.4",
                "cast": "Anthony Gonzalez, Gael García Bernal, Benjamin Bratt, Alanna Ubach, Renée Victor",
                "description": "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer.",
                "trailer_url": "https://www.youtube.com/watch?v=Ga6RYejo6Hk",
                "image_url": "https://m.media-amazon.com/images/M/MV5BYjQ5NjM0Y2YtNjZkNC00ZDhkLWJjMWItN2QyNzFkMDE3ZjAxXkEyXkFqcGdeQXVyODIxMzk5NjA@._V1_.jpg"
            },
            {
                "name": "Joker",
                "genre": "Drama",
                "language": "English",
                "rating": "8.4",
                "cast": "Joaquin Phoenix, Robert De Niro, Zazie Beetz, Frances Conroy, Brett Cullen",
                "description": "During the 1980s, a failed stand-up comedian is driven insane and turns to a life of crime and chaos in Gotham City while becoming an infamous psychopathic crime figure.",
                "trailer_url": "https://www.youtube.com/watch?v=zAGVQLHvwOY",
                "image_url": "https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg"
            },
            {
                "name": "Parasite",
                "genre": "Thriller",
                "language": "English",
                "rating": "8.6",
                "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik, Park So-dam",
                "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                "trailer_url": "https://www.youtube.com/watch?v=5xH0HfJHsaY",
                "image_url": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_.jpg"
            },
            {
                "name": "3 Idiots",
                "genre": "Comedy",
                "language": "Hindi",
                "rating": "8.4",
                "cast": "Aamir Khan, Madhavan, Sharman Joshi, Kareena Kapoor, Boman Irani",
                "description": "In the tradition of 'Educating Rita' and 'Dead Poets Society' comes this refreshing take on the 'college' genre. Two friends are searching for their long lost companion.",
                "trailer_url": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
                "image_url": "https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFkLTgwOTItNjI2Y2IyYzEwM2Y1XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
            },
            {
                "name": "Dangal",
                "genre": "Drama",
                "language": "Hindi",
                "rating": "8.3",
                "cast": "Aamir Khan, Sakshi Tanwar, Fatima Sana Shaikh, Sanya Malhotra, Zaira Wasim",
                "description": "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.",
                "trailer_url": "https://www.youtube.com/watch?v=x_7YlGv9u1g",
                "image_url": "https://m.media-amazon.com/images/M/MV5BMTQ4MzQzMzM2Nl5BMl5BanBnXkFtZTgwMTQ1NzU3MDI@._V1_.jpg"
            },
            {
                "name": "RRR",
                "genre": "Action",
                "language": "Telugu",
                "rating": "8.0",
                "cast": "N.T. Rama Rao Jr., Ram Charan, Ajay Devgn, Alia Bhatt, Shriya Saran",
                "description": "A fictional story about two legendary revolutionaries and their journey away from home before they started fighting for their country in 1920s.",
                "trailer_url": "https://www.youtube.com/watch?v=f_vbAtFSEc0",
                "image_url": "https://m.media-amazon.com/images/M/MV5BODUwNDNjYzctODUxNy00ZTA2LWIyYTEtMDc5Y2E5ZjBmNTMzXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg"
            },
            {
                "name": "Baahubali: The Beginning",
                "genre": "Action",
                "language": "Telugu",
                "rating": "8.0",
                "cast": "Prabhas, Rana Daggubati, Anushka Shetty, Tamannaah Bhatia, Ramya Krishnan",
                "description": "In ancient India, an adventurous and daring man becomes involved in a decades-old feud between two warring peoples.",
                "trailer_url": "https://www.youtube.com/watch?v=sOEg_YZQsTI",
                "image_url": "https://m.media-amazon.com/images/M/MV5BYmJhMGVkYmQtOWY4Ny00YjY0LThkNjctOGI5OWYyY2Y4YjY3XkEyXkFqcGdeQXVyNTgxODY5ODI@._V1_.jpg"
            },
            {
                "name": "K.G.F: Chapter 1",
                "genre": "Action",
                "language": "Kannada",
                "rating": "8.2",
                "cast": "Yash, Srinidhi Shetty, Ramachandra Raju, Archana Jois, Achyuth Kumar",
                "description": "In the 1970s, a fierce rebel rises against the brutal oppression that the poor people living in the Kolar Gold Fields have been facing.",
                "trailer_url": "https://www.youtube.com/watch?v=qXgF-iJ_ezE",
                "image_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"
            },
            {
                "name": "Vikram",
                "genre": "Action",
                "language": "Tamil",
                "rating": "8.3",
                "cast": "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil, Narain, Kalidas Jayaram",
                "description": "A special agent investigates a murder committed by a masked group of serial killers called 'Vikram' and discovers a conspiracy.",
                "trailer_url": "https://www.youtube.com/watch?v=OKBMCL-frPU",
                "image_url": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"
            },
            {
                "name": "Drishyam",
                "genre": "Thriller",
                "language": "Hindi",
                "rating": "8.2",
                "cast": "Ajay Devgn, Tabu, Shriya Saran, Ishita Dutta, Mrunal Jadhav",
                "description": "A man goes to extreme lengths to save his family from punishment after the family commits an accidental crime.",
                "trailer_url": "https://www.youtube.com/watch?v=Auu6rxo34QQ",
                "image_url": "https://m.media-amazon.com/images/M/MV5BYmJhMGVkYmQtOWY4Ny00YjY0LThkNjctOGI5OWYyY2Y4YjY3XkEyXkFqcGdeQXVyNTgxODY5ODI@._V1_.jpg"
            },
        ]

        created = 0
        updated = 0
        
        for m in movies_to_seed:
            defaults = {
                "genre": m["genre"],
                "language": m["language"],
                "rating": m["rating"],
                "cast": m["cast"],
                "description": m["description"],
                "trailer_url": m.get("trailer_url", ""),
            }
            
            obj, was_created = Movie.objects.update_or_create(name=m["name"], defaults=defaults)
            
            # Download and save image if URL provided
            if m.get("image_url") and not obj.image:
                try:
                    self.stdout.write(f"Downloading image for {m['name']}...")
                    response = requests.get(m["image_url"], timeout=10, stream=True)
                    if response.status_code == 200:
                        # Get file extension from URL
                        parsed_url = urlparse(m["image_url"])
                        file_ext = os.path.splitext(parsed_url.path)[1] or '.jpg'
                        
                        # Create media directory if it doesn't exist
                        media_path = os.path.join(settings.MEDIA_ROOT, 'movies')
                        os.makedirs(media_path, exist_ok=True)
                        
                        # Save image
                        filename = f"{obj.id}_{obj.name.replace(' ', '_')}{file_ext}"
                        filepath = os.path.join(media_path, filename)
                        
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        # Update movie with image
                        obj.image.name = f'movies/{filename}'
                        obj.save()
                        self.stdout.write(self.style.SUCCESS(f"  [OK] Image saved for {m['name']}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"  [WARN] Could not download image for {m['name']} (Status: {response.status_code})"))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  [WARN] Error downloading image for {m['name']}: {str(e)}"))
            
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"\n[SUCCESS] Seed complete. Created: {created}, Updated: {updated}"))
        self.stdout.write(self.style.SUCCESS("Movies are now ready with detailed information and images!"))
