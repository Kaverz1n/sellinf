from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, ConfirmationCodeView

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('confirmation/<int:user_id>/', ConfirmationCodeView.as_view(), name='confirmation_account'),
]
