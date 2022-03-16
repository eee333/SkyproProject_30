from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads import views
from ads.views import CategoryViewSet
from users.views import LocationViewSet

router = routers.SimpleRouter()
router.register('location', LocationViewSet)
router.register('category', CategoryViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.index),
    path('ad/', include('ads.urls')),
    path('user/', include('users.urls')),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
