from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label = '', help_text='<small>Enter your e-mail</small>',  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    # def clean(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('The two password fields must be equal')
    #     return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].help_text = '<small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>'
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<small><ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul></small>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Verify Password'
        self.fields['password2'].help_text = ''
        self.fields['password2'].help_text = '<small><ul><li>Enter the same password as before, for verification.</li></ul></small>'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class GenUser(forms.Form):
    username = forms.CharField(max_length=100)
    # password = forms.CharField(widget=forms.PasswordInput)


class MyAuthForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        field = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False

        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password'].label = False
