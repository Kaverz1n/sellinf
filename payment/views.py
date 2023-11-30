import stripe

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from payment.models import Payment
from sellinf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutSessionView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    '''
    Create a checkout session and redirect the user
    '''

    def get(self, request, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 999,
                        'product_data': {
                            'name': 'SELLINF SUBSCRIPTION',
                            'description': 'Upgrading user account to view premium content',
                        },
                    },
                    'quantity': 1
                }
            ],
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL
        )

        Payment.objects.create(
            user=request.user,
            date=checkout_session.created,
            checkout_id=checkout_session.id
        )

        return redirect(checkout_session.url)

    def test_func(self) -> bool:
        return not self.request.user.is_upgraded

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:content_list'))


class SuccessTemplateView(LoginRequiredMixin, generic.TemplateView):
    '''
    Success view
    '''
    extra_context = {'title': 'Success'}

    def dispatch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            checkout_id = Payment.objects.filter(user=user).order_by('-date').first().checkout_id
            session = stripe.checkout.Session.retrieve(checkout_id)

            if not session.payment_status == 'paid':
                return redirect(reverse('payment:cancel'))

            return super().dispatch(request, *args, **kwargs)
        except:
            return redirect(reverse('content:upgrade'))

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user.is_upgraded = True
        user.save()

        messages.success(self.request, 'You have successfully upgraded your account!')

        return redirect(reverse('content:content_list'))


class CancelTemplateView(LoginRequiredMixin, generic.TemplateView):
    '''
    Success view
    '''
    extra_context = {'title': 'Cancel'}

    def dispatch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            checkout_id = Payment.objects.get(user=user).checkout_id
            session = stripe.checkout.Session.retrieve(checkout_id)

            if session.payment_status == 'paid':
                return redirect(reverse('content:content_list'))

            return super().dispatch(request, *args, **kwargs)
        except:
            return redirect(reverse('content:upgrade'))

    def get(self, request, *args, **kwargs):
        messages.error(self.request, 'Something went wrong. Please try to upgrade your account again!')

        return redirect(reverse('content:content_list'))
