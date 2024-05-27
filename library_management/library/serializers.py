from rest_framework import serializers
from .models import User, Author, Genre, Book, Rental
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'personal_number', 'birth_date', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'full_name', 'birth_date']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genres', 'release_date', 'amount_in_stock', 'times_rented']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        genres_data = validated_data.pop('genres')
        author, _ = Author.objects.get_or_create(**author_data)
        book = Book.objects.create(author=author, **validated_data)
        for genre_data in genres_data:
            genre, _ = Genre.objects.get_or_create(**genre_data)
            book.genres.add(genre)
        return book


class RentalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookSerializer()

    class Meta:
        model = Rental
        fields = ['id', 'user', 'book', 'rent_date', 'return_date']
