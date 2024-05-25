from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthorViewSet, GenreViewSet, BookViewSet, RentalViewSet, top_books, top_late_books, top_late_customers

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('statistics/top-books/', top_books, name='top_books'),
    path('statistics/top-late-books/', top_late_books, name='top_late_books'),
    path('statistics/top-late-customers/', top_late_customers, name='top_late_customers'),
]

