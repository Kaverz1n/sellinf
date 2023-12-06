from content.apps import ContentConfig
from content.views import (
    IndexView, ContentListView, FoundContentListView, AboutTemplateView, UpgradeTemplateView,
    ContentDetailView, ContentCreateView, UserContentListView, ContentUpdateView, ContentDeleteView,
    ContentPublishStatusView, ModeratorContentListView
)

from django.views.decorators.cache import cache_page
from django.urls import path

app_name = ContentConfig.name

urlpatterns = [
    path('', cache_page(100 * 60)(IndexView.as_view()), name='index'),
    path('contents/', ContentListView.as_view(), name='content_list'),
    path('contents/<str:search_query>/', FoundContentListView.as_view(), name='found_content_list'),
    path('content/<int:pk>/publications/', UserContentListView.as_view(), name='user_content_list'),
    path('content/check/', ModeratorContentListView.as_view(), name='moderator_content_list'),
    path('content/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
    path('content/create/', ContentCreateView.as_view(), name='content_create'),
    path('content/<int:pk>/update/', ContentUpdateView.as_view(), name='content_update'),
    path('content/<int:pk>/delete/', ContentDeleteView.as_view(), name='content_delete'),
    path('content/<int:pk>/publish/', ContentPublishStatusView.as_view(), name='content_publish_status'),
    path('about/', cache_page(100 * 60)(AboutTemplateView.as_view()), name='about'),
    path('upgrade/', cache_page(100 * 60)(UpgradeTemplateView.as_view()), name='upgrade'),
]
