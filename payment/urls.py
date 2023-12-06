from django.urls import path

from payment.apps import PaymentConfig
from payment.views import CheckoutSessionView, SuccessTemplateView, CancelTemplateView

app_name = PaymentConfig.name

urlpatterns = [
    path('checkout/', CheckoutSessionView.as_view(), name='checkout_session'),
    path('success/', SuccessTemplateView.as_view(), name='success'),
    path('cancel/', CancelTemplateView.as_view(), name='cancel'),
]
