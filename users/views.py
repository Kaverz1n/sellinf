from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from users.forms import UserRegisterForm, ConfirmationCodeForm, AuthorizationForm
from users.models import User
from users.services import code_generation


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

            code_generation(self.object)

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

            return redirect(reverse('content:content_list'))

        return render(
            request,
            'users/confirmation_account.html',
            {
                'title': 'Confirmation Code',
                'form': form,
            }
        )


class AuthorizationView(generic.View):
    '''
    Authorize user by phone number
    '''

    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = AuthorizationForm()

        return render(
            request,
            'users/authorization.html',
            {
                'title': 'Authorization',
                'form': form,
            }
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = AuthorizationForm(request.POST)

        if form.is_valid():
            self.object = User.objects.get(phone=form.cleaned_data['phone'])
            code_generation(self.object)

            return redirect(reverse('users:confirmation_account', kwargs={'user_id': self.object.id}))

        return render(
            request,
            'users/authorization.html',
            {
                'title': 'Authorization',
                'form': form,
            }
        )
