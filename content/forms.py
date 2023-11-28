from django import forms


class SearchForm(forms.Form):
    '''
    Search form class
    '''
    search_query = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs) -> None:
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search_query'].label = ''
