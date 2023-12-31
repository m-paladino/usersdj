from django.urls import path
from . import views

app_name = 'users_app'

urlpatterns = [
    path(
        'register/',
        views.UserRegisterView.as_view(),
        name='register'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'update_password/',
        views.UpdatePasswordView.as_view(),
        name='update_password'
    ),
    path(
        'validate/<pk>/',
        views.UserVerificationView.as_view(),
        name='validate'
    ),
]
