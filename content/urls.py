from content.apps import ContentConfig
from content.views import IndexView, ContentListView, FoundContentListView, AboutTemplateView, UpgradeTemplateView, \
    ContentDetailView

from django.urls import path

app_name = ContentConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contents/', ContentListView.as_view(), name='content_list'),
    path('contents/<str:search_query>/', FoundContentListView.as_view(), name='found_content_list'),
    path('content/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('upgrade/', UpgradeTemplateView.as_view(), name='upgrade'),
]
