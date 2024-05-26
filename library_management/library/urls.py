from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'rentals', views.RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),  # No need to nest `api/` here, it's already included in the project `urls.py`
    path('top-books/', views.top_books, name='top-books'),
    path('top-late-books/', views.top_late_books, name='top-late-books'),
    path('top-late-customers/', views.top_late_customers, name='top-late-customers'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('books/', views.book_list, name='book_list'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),
    path('borrow/<int:pk>/', views.BookViewSet.as_view({'post': 'borrow'}), name='borrow_book'),
    path('return/<int:pk>/', views.BookViewSet.as_view({'post': 'return_book'}), name='return_book'),
]
