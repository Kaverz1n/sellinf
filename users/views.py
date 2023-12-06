from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from users.forms import UserRegisterForm, ConfirmationCodeForm, AuthorizationForm, UserUpdateForm, UserDeleteAccountForm
from users.models import User, Subscription
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


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    '''
    User detail view
    '''
    model = User
    context_object_name = 'object'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        is_subscribed = Subscription.objects.filter(user_pk=self.object.id, subscriber=self.request.user).exists()

        context['title'] = f'{self.object.nickname}'
        context['is_subscribed'] = is_subscribed

        return context


class Subscribe(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    '''
    Class for subscribe on user
    '''

    def get(self, request, *args, **kwargs) -> HttpResponse:
        user = User.objects.get(pk=self.kwargs['pk'])

        if kwargs['status'] == 'subscribe':
            Subscription.objects.create(user_pk=self.kwargs['pk'], subscriber=self.request.user)
            user.subscribers += 1
            user.save()

            return redirect(reverse('users:user_detail', kwargs={'pk': self.kwargs['pk']}))

        Subscription.objects.filter(user_pk=self.kwargs['pk'], subscriber=self.request.user).delete()
        user.subscribers -= 1
        user.save()

        return redirect(reverse('users:user_detail', kwargs={'pk': self.kwargs['pk']}))

    def test_func(self) -> bool:
        return self.request.user.is_upgraded

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:upgrade'))


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    '''
    User update view
    '''
    model = User
    form_class = UserUpdateForm

    def get_success_url(self) -> str:
        messages.success(self.request, 'You have successfully updated your account!')
        return reverse('users:user_detail', kwargs={'pk': self.object.pk})

    def test_func(self) -> bool:
        return self.request.user == self.get_object()

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:content_list'))


class UserDeleteAccountView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    '''
    User delete account view
    '''
    model = User
    form_class = UserDeleteAccountForm

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.nickname}'

        return context

    def get_success_url(self) -> str:
        messages.success(self.request, 'You have successfully deleted your account!')
        return reverse('content:index')

    def test_func(self) -> bool:
        return self.request.user == self.get_object()

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:content_list'))
