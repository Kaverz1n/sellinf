from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sellinf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('content.urls', namespace='content')),
    path('users/', include('users.urls', namespace='users')),
    path('payment/', include('payment.urls', namespace='payment'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
