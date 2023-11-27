import random

from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from users.forms import UserRegisterForm, ConfirmationCodeForm
from users.models import User, ConfirmationCode
from users.tasks import send_confirmation_code


class UserRegisterView(generic.CreateView):
    '''
    Create a new user
    '''
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegisterForm

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.save()

            # create a confirmation code
            code = int(''.join([str(random.randint(1, 9)) for _ in range(4)]))
            try:
                ConfirmationCode.objects.create(user=self.object, code=code)
            except:
                users_code = ConfirmationCode.objects.get(user=self.object)
                users_code.code = code

            send_confirmation_code.delay(self.object.phone)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('users:confirmation_account', kwargs={'user_id': self.object.id})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'

        return context


class ConfirmationCodeView(generic.View):
    '''
    Confirm registration by code
    '''

    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = ConfirmationCodeForm()
        form.user_id = kwargs['user_id']

        return render(
            request,
            'users/confirmation_account.html',
            {
                'title': 'Confirmation Code',
                'form': form,
            }
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = ConfirmationCodeForm(request.POST)
        form.user_id = kwargs['user_id']

        if form.is_valid():
            user = User.objects.get(pk=kwargs['user_id'])
            user.is_active = True
            user.save()

            login(request, user)

            return redirect('content:index')

        return render(
            request,
            'users/confirmation_account.html',
            {
                'title': 'Confirmation Code',
                'form': form,
            }
        )

