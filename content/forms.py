from content.models import Content

from django import forms


class SearchForm(forms.Form):
    '''
    Search form class
    '''
    search_query = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs) -> None:
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search_query'].label = ''


class ContentForm(forms.ModelForm):
    '''
    Form to create content
    '''

    def __init__(self, *args, **kwargs) -> None:
        super(ContentForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ''
        self.fields['content'].label = ''
        self.fields['type'].label = ''

    class Meta:
        model = Content
        fields = (
            'title',
            'content',
            'type',
        )
