from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app import urls as urlpatterns
# from app import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urlpatterns)),
    path('api-auth/', include('rest_framework.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
