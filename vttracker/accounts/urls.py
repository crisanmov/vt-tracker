from django.urls import path, include
from django.conf.urls import url
from accounts.forms import CustomAuthForm
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=CustomAuthForm)),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html')),
    url(r'^register/$', views.register, name='register'),
]
