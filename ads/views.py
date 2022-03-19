from django.db.models import Count
from django.http import JsonResponse

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.serializers import CategorySerializer, AdSerializer, SelectionSerializer, SelectionDetailSerializer
from users.permissions import ReadOnlyOrAdminPermissionList, OwnerPermissionOne, \
    AdminPermissionOne, ModeratorPermissionOne


def index(request):

    return JsonResponse({"status": "ok"})


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdminPermissionList]


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def list(self, request, *args, **kwargs):

        if cat_list := request.GET.getlist("cat", []):
            self.queryset = self.queryset.filter(category_id__in=cat_list)
        if text := request.GET.get("text", None):
            self.queryset = self.queryset.filter(name__icontains=text)
        if location := request.GET.get("location", None):
            # self.queryset = self.queryset.filter(user__locations__name__icontains=location)
            self.queryset = self.queryset.annotate(Count('user')).filter(user__locations__name__icontains=location)
            # self.queryset = self.queryset.filter(user__locations__name__icontains=location)
        if price_from := request.GET.get("price_from", None):
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to := request.GET.get("price_to", None):
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [OwnerPermissionOne | ModeratorPermissionOne | AdminPermissionOne]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [OwnerPermissionOne | AdminPermissionOne]


class AdImageUploadView(UpdateAPIView):
    """Загрузка картинки возможна только в существующее объяввление
    и разрешена только автору объявления.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [OwnerPermissionOne]


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):  # Send name and items
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [OwnerPermissionOne | AdminPermissionOne]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [OwnerPermissionOne | AdminPermissionOne]
