from django.views.generic.edit import FormView
from django.views.generic import View
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    UserVerificationForm,
)
from .models import User
from .functions import generate_random_code


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        # Generate a random code
        cod = generate_random_code()
        
        created_user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            names=form.cleaned_data['names'],
            last_names=form.cleaned_data['last_names'],
            gender=form.cleaned_data['gender'],
            register_code=cod
        )
        print("created_user: ", created_user)
        # Send email
        subject = 'Activate your account'
        message = 'Verification code: ' + cod
        from_email = 'mpaladino@ignetworks.com'
        send_mail(subject, message, from_email, [form.cleaned_data['email'],])

        return HttpResponseRedirect(
            reverse(
                'users_app:validate',
                kwargs={'pk': created_user.id}
            )
        )


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


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        user = authenticate(
            username=self.request.user.username,
            password=form.cleaned_data['password']
        )
        if user:
            new_password = form.cleaned_data['password1']
            user.set_password(new_password)
            user.save()

        logout(self.request)

        return super(UpdatePasswordView, self).form_valid(form)


class UserVerificationView(FormView):
    template_name = 'users/validate.html'
    form_class = UserVerificationForm
    success_url = reverse_lazy('users_app:login')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(UserVerificationView, self).form_valid(form)
