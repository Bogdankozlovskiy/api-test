from django.contrib.auth.models import User
from django.db import models


class UserPhone(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="phone"
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name="номер телефона"
    )


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="books"
    )
    buyer = models.ManyToManyField(
        User,
        through="manage_book.UserBook",
        related_name="bought_books"
    )


class UserBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_book_saled")
    date = models.DateField(auto_now_add=True)
    count = models.PositiveIntegerField(default=1)
