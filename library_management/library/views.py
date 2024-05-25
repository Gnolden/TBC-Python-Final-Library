from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F, Count
from .models import User, Author, Genre, Book, Rental
from .serializers import UserSerializer, AuthorSerializer, GenreSerializer, BookSerializer, RentalSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import timedelta

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rent(self, request, pk=None):
        book = self.get_object()
        user = request.user
        if book.amount_in_stock > 0:
            book.amount_in_stock -= 1
            book.times_rented += 1
            book.save()
            rental = Rental.objects.create(user=user, book=book)
            return Response({'status': 'book rented'}, status=status.HTTP_200_OK)
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

@api_view(['GET'])
def top_books(request):
    top_books = Book.objects.order_by('-times_rented')[:10]
    serializer = BookSerializer(top_books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def top_late_books(request):
    top_late_books = Rental.objects.filter(
        return_date__gt=F('rent_date') + timedelta(days=1)
    ).values('book').annotate(
        late_count=Count('book')
    ).order_by('-late_count')[:100]
    book_ids = [item['book'] for item in top_late_books]
    books = Book.objects.filter(id__in=book_ids)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def top_late_customers(request):
    top_late_customers = Rental.objects.filter(
        return_date__gt=F('rent_date') + timedelta(days=1)
    ).values('user').annotate(
        late_count=Count('user')
    ).order_by('-late_count')[:100]
    user_ids = [item['user'] for item in top_late_customers]
    users = User.objects.filter(id__in=user_ids)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
