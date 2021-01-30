import datetime
from typing import Any
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from manage_book.models import Book, UserBook
from manage_book.serializers import UserSerializer, BookSerializer
from uuid import uuid4
from django.conf import settings


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() and request.data.get("phone"):
            password = uuid4().__str__()
            user = serializer.save(phone=request.data.get("phone"), password=password)
            send_mail(
                "the password",
                f"password is {password}",
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.error_messages,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginUser(APIView):
    def post(self, request):
        user = auth.authenticate(
            request,
            username=request.data['email'],
            password=request.data['password']
        )
        if user is not None:
            login(request, user)
            return Response({}, status=status.HTTP_201_CREATED)
        return Response("this user is not exists", status=status.HTTP_400_BAD_REQUEST)


class MyPaginator(PageNumberPagination):
    page_size = 20


class ListCreateBook(ListCreateAPIView):
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    pagination_class = MyPaginator
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["title", "id", "author__first_name"]

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data.update(author=request.user.id)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.error_messages,
            status=status.HTTP_400_BAD_REQUEST
        )


class Statistic(APIView):
    def get(self, request):
        all_books = UserBook.objects.count()
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        last_month_book = UserBook.objects.filter(date__month=last_month.strftime("%Y%m"))
        each_author = User.objects.aggregate(Sum("user_book_saled__count"))
        return Response({
            "all_books": all_books,
            "last_month_book": last_month_book,
            "each_author": each_author
        },
            status=status.HTTP_200_OK
        )
