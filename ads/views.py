from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad
from ads.serializers import CategorySerializer, AdSerializer


def index(request):

    return JsonResponse({"status": "ok"})


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
    """
    Создание пользователя с локацией по названию.
    Если такой локации нет, то она будет создана.
    Локации передаются списком названий.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES["image"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "user_id": self.object.user_id,
            "image": self.object.image.url,
        })
