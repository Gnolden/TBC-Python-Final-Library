from django.contrib import admin
from django.db.models import Count

from .models import User, Author, Genre, Book, Rental

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'personal_number', 'birth_date')
    search_fields = ('full_name', 'email', 'personal_number')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date')
    search_fields = ('full_name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'release_date', 'amount_in_stock', 'times_rented')
    search_fields = ('title', 'author__full_name')
    list_filter = ('genres', 'release_date')
    filter_horizontal = ('genres',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_rentals=Count('rentals'))
        return queryset

    def times_rented(self, obj):
        return obj.num_rentals

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rent_date', 'return_date')
    search_fields = ('user__full_name', 'book__title')
    list_filter = ('rent_date', 'return_date')

# user irakli
# pass test123123