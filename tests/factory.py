import factory

from ads.models import Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "1234"
    email = factory.Faker("email")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "Test name 2"
    price = "200"
    description = "Test description"
    user = factory.SubFactory(UserFactory)
