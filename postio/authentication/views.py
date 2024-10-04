from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from .forms import RegistrationForm


# Create your views here.
class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    success_url = reverse_lazy('homepage')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')


