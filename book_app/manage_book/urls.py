from django.urls import path
from manage_book.views import RegisterUser, LoginUser, ListCreateBook

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register-user"),
    path("login/", LoginUser.as_view(), name="login-user"),
    path("list_create_book/", ListCreateBook.as_view(), name="list-create-book")
]
