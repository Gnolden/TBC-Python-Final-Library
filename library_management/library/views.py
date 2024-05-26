from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import LoginForm
from .forms import UserRegistrationForm
from .models import User, Author, Genre, Book, Rental
from .serializers import UserSerializer, AuthorSerializer, GenreSerializer, BookSerializer, RentalSerializer


# User registration view
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})


# User login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("book_list")
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", { "form": form })


# User logout view
def logout_user(request):
    logout(request)
    return redirect('login')


# Book list view for customers
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


# Borrowed books view for customers
@login_required
def borrowed_books(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'borrowed_books.html', {'rentals': rentals})


# Viewsets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genres', 'release_date']
    search_fields = ['title', 'author__full_name']
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def borrow(self, request, pk=None):
        book = self.get_object()
        user = request.user
        if book.amount_in_stock > 0:
            book.amount_in_stock -= 1
            book.times_rented += 1
            book.save()
            rental = Rental.objects.create(user=user, book=book)
            return Response({'status': 'book borrowed'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'no stock'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        book = self.get_object()
        user = request.user
        rental = Rental.objects.filter(user=user, book=book, return_date__isnull=True).first()
        if rental:
            rental.return_date = timezone.now()
            rental.save()
            book.amount_in_stock += 1
            book.save()
            return Response({'status': 'book returned'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'no active rental'}, status=status.HTTP_400_BAD_REQUEST)


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]


# Statistics views
@api_view(['GET'])
def top_books(request):
    top_books = Book.objects.order_by('-times_rented')[:10]
    serializer = BookSerializer(top_books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_late_books(request):
    from datetime import timedelta
    from django.db.models import Count, F
    late_books = Rental.objects.filter(return_date__gt=F('rent_date') + timedelta(days=1)).values('book').annotate(
        late_count=Count('book')).order_by('-late_count')[:100]
    book_ids = [item['book'] for item in late_books]
    books = Book.objects.filter(id__in=book_ids)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_late_customers(request):
    from datetime import timedelta
    from django.db.models import Count, F
    late_customers = Rental.objects.filter(return_date__gt=F('rent_date') + timedelta(days=1)).values('user').annotate(
        late_count=Count('user')).order_by('-late_count')[:100]
    user_ids = [item['user'] for item in late_customers]
    users = User.objects.filter(id__in=user_ids)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
