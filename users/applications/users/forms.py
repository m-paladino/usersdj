from django import forms
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