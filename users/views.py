from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Location, User
from users.permissions import OwnerPermissionOne, AdminPermissionOne, ModeratorPermissionOne, \
    AdminPermissionList, ModeratorPermissionList, ReadOnlyOrAdminPermissionList, OwnerUserPermissionOne
from users.serializers import UserSerializer, LocationSerializer, UserCrateSerializer, \
    UserUpdateSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [ReadOnlyOrAdminPermissionList]


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ModeratorPermissionList | AdminPermissionList]


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OwnerUserPermissionOne | ModeratorPermissionOne | AdminPermissionOne]


class UserCreateView(CreateAPIView):
    """
    Создание пользователя с локацией по названию.
    Если такой локации нет, то она будет создана.
    Локации передаются списком названий.
    """
    queryset = User.objects.all()
    serializer_class = UserCrateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [OwnerUserPermissionOne | ModeratorPermissionOne | AdminPermissionOne]


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OwnerUserPermissionOne | AdminPermissionOne]
