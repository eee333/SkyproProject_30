from rest_framework import serializers
from users.models import User, Location


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

    class Meta:
        model = User
        fields = '__all__'

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

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
