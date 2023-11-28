from django.db.models import QuerySet, Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from content.forms import SearchForm
from content.models import Content


class IndexView(generic.TemplateView):
    '''
    Index page view
    '''
    template_name = 'content/index.html'
    extra_context = {'title': 'Sellinf'}


class ContentListView(generic.ListView):
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

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        search_query = self.kwargs.get('search_query')

        queryset = Content.objects.filter(
            Q(is_published=True) &
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        context['form'] = SearchForm(self.request.GET)

        return context
