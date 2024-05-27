import random
from django.core.management.base import BaseCommand
from library.models import Author, Genre, Book, User

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.create_authors()
        self.create_genres()
        self.create_books()

    def create_authors(self):
        for i in range(10):
            Author.objects.create(
                full_name=f'Author {i}',
                birth_date=f'19{random.randint(50, 99)}-01-01'
            )

    def create_genres(self):
        genres = ['Science Fiction', 'Fantasy', 'Mystery', 'Thriller', 'Romance', 'Western', 'Dystopian', 'Contemporary']
        for genre in genres:
            Genre.objects.create(name=genre)

    def create_books(self):
        authors = Author.objects.all()
        genres = Genre.objects.all()
        for i in range(1000):
            release_year = random.randint(1950, 2023)  # Adjusted range to ensure valid years
            release_date = f'{release_year}-01-01'
            book = Book.objects.create(
                title=f'Book {i}',
                author=random.choice(authors),
                release_date=release_date,
                amount_in_stock=random.randint(1, 10),
                times_rented=random.randint(0, 100)
            )
            book.genres.set(random.sample(list(genres), k=random.randint(1, 3)))
            book.save()
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))
