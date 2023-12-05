from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import TextInput

from users.models import User, ConfirmationCode


class UserRegisterForm(UserCreationForm):
    '''
    Form to register a new user
    '''

    class Meta:
        model = User
        fields = ('phone', 'nickname',)
        widgets = {
            'phone': TextInput(attrs={'placeholder': 'Enter your phone...'}),
            'nickname': TextInput(attrs={'placeholder': 'Enter your nickname...'}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['phone'].label = ''
        self.fields['nickname'].label = ''
        self.fields.pop('password1')
        self.fields.pop('password2')

    def clean(self) -> dict:
        cleaned_data = super().clean()

        # ignore the password1 and password2 fields
        cleaned_data['password1'] = None
        cleaned_data['password2'] = None

        return cleaned_data

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get('phone')

        if not phone[1:].isdigit():
            raise forms.ValidationError('Phone number must be digital')

        if phone[:1] != '+':
            raise forms.ValidationError('Phone number must start with +')

        return phone


class ConfirmationCodeForm(forms.Form):
    '''
    Form to confirm registration by code
    '''
    code = forms.IntegerField(widget=TextInput(attrs={'placeholder': 'Enter confirm code...', 'step': 1}))

    def __init__(self, *args, **kwargs) -> None:
        super(ConfirmationCodeForm, self).__init__(*args, **kwargs)
        self.fields['code'].label = ''
        self.user_id = kwargs.get('user_id')

    def clean_code(self, *args, **kwargs) -> str:
        code = self.cleaned_data['code']
        user_code = ConfirmationCode.objects.get(user_id=self.user_id).code

        if code != user_code:
            raise forms.ValidationError('Invalid code')

        return code


class AuthorizationForm(forms.Form):
    '''
    Form to authorize user
    '''
    phone = forms.CharField(max_length=15, widget=TextInput(attrs={'placeholder': 'Enter your phone...'}))

    def __init__(self, *args, **kwargs) -> None:
        super(AuthorizationForm, self).__init__(*args, **kwargs)
        self.fields['phone'].label = ''

    def clean_phone(self, *args, **kwargs) -> str:
        phone = self.cleaned_data['phone']

        if not phone[1:].isdigit():
            raise forms.ValidationError('Phone number must be digital')

        if phone[:1] != '+':
            raise forms.ValidationError('Phone number must start with +')

        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('User not found')

        return phone


class UserUpdateForm(forms.ModelForm):
    '''
    Form to update user
    '''

    def __init__(self, *args, **kwargs) -> None:
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['nickname'].label = ''
        self.fields['nickname'].widget.attrs['placeholder'] = 'Enter your nickname...'
        self.fields['about'].label = ''
        self.fields['about'].widget.attrs['placeholder'] = 'Enter about yourself...'
        self.fields['image'].label = ''

    class Meta:
        model = User
        fields = ('nickname', 'about', 'image')


class UserDeleteAccountForm(forms.Form):
    '''
    Form to delete user
    '''
    confirm_delete = forms.CharField(max_length=30, widget=TextInput(attrs={'placeholder': 'Are you sure...?'}))

    def __init__(self, *args, **kwargs) -> None:
        super(UserDeleteAccountForm, self).__init__(*args, **kwargs)
        self.fields['confirm_delete'].label = ''

    def clean_confirm_delete(self, *args, **kwargs) -> str:
        confirm_delete = self.cleaned_data['confirm_delete']

        if confirm_delete != 'I want to delete my account!':
            raise forms.ValidationError('That\' not right!')

        return confirm_delete
