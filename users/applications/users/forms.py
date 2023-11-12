from django import forms
from django.contrib.auth import authenticate
from .models import User


class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )

    password2 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your password'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'names', 'last_names', 'gender')


    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Passwords do not match')


    def clean_password1(self):
        if len(self.cleaned_data['password1']) < 5:
            self.add_error('password1', 'Password must be at least 5 characters long')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password'
            }
        )
    )


    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('The username and/or password are incorrect')

        return self.cleaned_data


class UpdatePasswordForm(forms.Form):

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password'
            }
        )
    )

    password1 = forms.CharField(
        label='New Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your new password'
            }
        )
    )

    password2 = forms.CharField(
        label='Repeat New Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your new password'
            }
        )
    )


    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)


    def clean_password(self):
        password = self.cleaned_data['password']
        user = authenticate(
            username=self.current_user.username,
            password=password
        )
        if not user:
            raise forms.ValidationError('The password is incorrect')

        return password


    def clean_password1(self):
        if len(self.cleaned_data['password1']) < 5:
            self.add_error('password1', 'Password must be at least 5 characters long')
        # if self.cleaned_data['password1'] is not returned here, it wont exist
        # in the cleaned_data dictionary, so it wont be accessible in clean_password2
        return self.cleaned_data['password1']


    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Passwords do not match')
        return self.cleaned_data['password2']
