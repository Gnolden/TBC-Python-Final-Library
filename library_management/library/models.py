from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.full_name

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.full_name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField()
    amount_in_stock = models.PositiveIntegerField()
    times_rented = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, related_name='rentals', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='rentals', on_delete=models.CASCADE)
    rent_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.full_name} - {self.book.title}'
