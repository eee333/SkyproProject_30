import factory

from ads.models import Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "member"
    password = "1234"
    email = "qqq@qqq.qq"


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "Test name 2"
    price = "200"
    description = "Test description"
    user = factory.SubFactory(UserFactory)
