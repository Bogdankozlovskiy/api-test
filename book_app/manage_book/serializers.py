from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, CharField
from manage_book.models import UserPhone, Book, UserBook


class PhoneSerializer(ModelSerializer):
    class Meta:
        model = UserPhone
        fields = ['phone_number']


class UserSerializer(ModelSerializer):
    phone = PhoneSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone"
        ]

    def save(self, phone, password):
        user = super().save(
            username=self.validated_data['email']
        )
        user.set_password(password)
        user.save()
        UserPhone.objects.create(
            user=user,
            phone_number=phone
        )
        return user


class BookSerializer(ModelSerializer):
    author = CharField(source="author.first_name")

    class Meta:
        model = Book
        fields = "__all__"

    def save(self):
        Book.objects.create(
            title=self.validated_data['title'],
            author_id=self.validated_data['author']['last_name']
        )


class UserBookSerializer(ModelSerializer):
    class Meta:
        model = UserBook
        fields = ['book_id', "count"]
