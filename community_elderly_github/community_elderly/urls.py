from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),  # 改成 django-admin，避免冲突
    path('', include('elderly_system.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
