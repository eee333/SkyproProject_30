from datetime import date

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User, Location


def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
    if not full_year_passed:
        age -= 1
    return age


class CheckRumblerEmail:
    def __call__(self, value):
        if value.endswith("rambler.ru"):
            raise serializers.ValidationError("rambler.ru not allowed")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    """locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )"""

    class Meta:
        model = User
        exclude = ["password"]


class UserCrateSerializer(serializers.ModelSerializer):

    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=True,
        slug_field='name'
    )
    email = serializers.EmailField(validators=[CheckRumblerEmail()])

    class Meta:
        model = User
        fields = '__all__'

    def validate_birth_date(self, value):
        if calculate_age(value) < 9:
            raise serializers.ValidationError("At least 9 years old")
        return value

    def is_valid(self, raise_exception=False):
        self._locations = []
        if self.initial_data.get("locations"):
            self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = super().create(validated_data)

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)

        user.set_password(user.password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[CheckRumblerEmail()])

    class Meta:
        model = User
        fields = '__all__'

    def validate_birth_date(self, value):
        if calculate_age(value) < 9:
            raise serializers.ValidationError("Incorrect dismiss date")
        return value

    def save(self):
        if password := self.validated_data.get('password'):
            self.validated_data['password'] = make_password(password)
        return super().save()
