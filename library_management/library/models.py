from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Provide default values for additional fields if not provided
        extra_fields.setdefault('full_name', 'Superuser')
        extra_fields.setdefault('personal_number', '0000000000')
        extra_fields.setdefault('birth_date', '1970-01-01')  # Some default date

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='library_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='library_user_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    objects = UserManager()

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
