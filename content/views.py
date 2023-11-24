from django.views import generic


class IndexView(generic.TemplateView):
    '''
    Index page view
    '''
    template_name = 'content/index.html'
