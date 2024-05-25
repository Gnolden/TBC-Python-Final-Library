from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthorViewSet, GenreViewSet, BookViewSet, RentalViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
