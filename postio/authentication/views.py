from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy


# Create your views here.

class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    success_url = reverse_lazy('homepage')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')
