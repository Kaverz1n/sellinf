from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserRegisterView, ConfirmationCodeView, AuthorizationView, UserDetailView, UserUpdateView,
    UserDeleteAccountView
)

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('confirmation/<int:user_id>/', ConfirmationCodeView.as_view(), name='confirmation_account'),
    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete_account/', UserDeleteAccountView.as_view(), name='user_delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
