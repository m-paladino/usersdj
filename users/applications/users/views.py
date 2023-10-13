from django.views.generic.edit import FormView
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, LoginForm
from .models import User


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            names=form.cleaned_data['names'],
            last_names=form.cleaned_data['last_names'],
            gender=form.cleaned_data['gender'],
        )
        return super(UserRegisterView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)

        return super(LoginView, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kwarg):
        logout(request)

        return HttpResponseRedirect(
            reverse(
                'users_app:login'
            )
        )
