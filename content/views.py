from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet, Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from content.forms import SearchForm, ContentForm
from content.models import Content


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


class ContentCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    '''
    Content create view
    '''
    model = Content
    form_class = ContentForm
    extra_context = {'title': 'Create content'}

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

            return super().form_valid(form)

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


class UserContentListView(UserPassesTestMixin, ContentListView):
    '''
    User content list view
    '''
    template_name = 'content/user_content_list.html'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title

        return context


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
