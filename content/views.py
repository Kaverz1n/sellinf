from content.forms import SearchForm, ContentForm
from content.models import Content

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.db.models import QuerySet, Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic


class IndexView(UserPassesTestMixin, generic.TemplateView):
    '''
    Index page view
    '''
    template_name = 'content/index.html'
    extra_context = {'title': 'Sellinf'}

    def test_func(self) -> bool:
        return self.request.user.is_anonymous

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:content_list'))


class ContentCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    '''
    Content create view
    '''
    model = Content
    form_class = ContentForm
    permission_required = 'content.add_content'

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

            return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create new content'
        context['text'] = 'CREATING'
        context['button_text'] = 'CREATE'

        return context

    def get_success_url(self) -> str:
        messages.info(self.request, 'Content will be published after verification by a moderator!')
        return reverse('content:content_list')

    def test_func(self) -> bool:
        return self.request.user.is_upgraded

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:upgrade'))


class ContentListView(LoginRequiredMixin, generic.ListView):
    '''
    Content list view
    '''
    model = Content

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by('-views')[:5]

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Sellinf'
        context['form'] = SearchForm(self.request.GET)

        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = SearchForm(self.request.POST)

        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            if search_query:
                return redirect(
                    reverse(
                        'content:found_content_list',
                        kwargs={'search_query': search_query}
                    )
                )

        return redirect(reverse('content:content_list'))


class FoundContentListView(ContentListView):
    '''
    Found content list view
    '''
    paginate_by = 5

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        search_query = self.kwargs.get('search_query')

        queryset = Content.objects.filter(
            Q(is_published=True) &
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        ).order_by('-views', 'id')

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        context['form'] = SearchForm(self.request.GET)

        return context


class UserContentListView(UserPassesTestMixin, PermissionRequiredMixin, ContentListView):
    '''
    User content list view
    '''
    template_name = 'content/user_content_list.html'
    permission_required = 'content.add_content'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        queryset = Content.objects.filter(owner=self.request.user)

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f'{self.request.user.nickname}\'s content'
        context['form'] = ''

        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        pass

    def test_func(self) -> bool:
        return self.request.user.is_upgraded

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:upgrade'))


class ModeratorContentListView(UserPassesTestMixin, ContentListView):
    '''
    Moderator content list view
    '''
    template_name = 'content/moderator_content_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        queryset = Content.objects.filter(is_published=False)

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f'Checking content'
        context['form'] = ''

        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        pass

    def test_func(self) -> bool:
        group = self.request.user.groups.filter(name='moderator').exists()

        return group

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:upgrade'))


class ContentPublishStatusView(generic.View):
    '''
    Class for change publish status of content
    '''

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.object = Content.objects.get(pk=self.kwargs['pk'])
        self.object.is_published = True
        self.object.save()

        return redirect(reverse('content:moderator_content_list'))


class ContentDetailView(LoginRequiredMixin, generic.DetailView):
    '''
    Content detail view
    '''
    model = Content

    def get_object(self, queryset=None) -> Content:
        self.object = super().get_object(queryset=queryset)
        self.object.views += 1
        self.object.save()

        return self.object

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.title}'

        return context


class ContentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    '''
    Content update view
    '''
    model = Content
    form_class = ContentForm
    permission_required = 'content.change_content'

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            self.object = form.save()
            self.object.is_published = False
            self.object.save()

            return super().form_valid(form)

    def get_success_url(self) -> str:
        messages.info(self.request, 'Content will be updated after verification by a moderator!')
        return reverse('content:content_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.title}'
        context['text'] = 'UPDATING'
        context['button_text'] = 'UPDATE'

        return context

    def test_func(self) -> bool:
        return self.request.user == self.get_object().owner

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:upgrade'))


class ContentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    '''
    Content delete view
    '''
    model = Content
    permission_required = 'content.delete_content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.title}'

        return context

    def get_success_url(self) -> str:
        messages.success(self.request, 'Content have been successfully deleted!')

        moderator = self.request.user.groups.filter(name='moderator')

        if moderator:
            return reverse('content:moderator_content_list')

        return reverse('content:content_list')

    def test_func(self) -> bool:
        owner = self.request.user == self.get_object().owner
        moderator = self.request.user.groups.filter(name='moderator') and not self.get_object().is_published

        return owner or moderator

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:upgrade'))


class AboutTemplateView(LoginRequiredMixin, generic.TemplateView):
    '''
    About template view
    '''
    template_name = 'content/about.html'
    extra_context = {'title': 'About'}


class UpgradeTemplateView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    '''
    Upgrade template view
    '''
    template_name = 'content/upgrade.html'
    extra_context = {'title': 'Upgrade'}

    def test_func(self) -> bool:
        return not self.request.user.is_upgraded

    def handle_no_permission(self) -> HttpResponse:
        return redirect(reverse('content:content_list'))
