from content.apps import ContentConfig
from content.views import IndexView

from django.urls import path

app_name = ContentConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
