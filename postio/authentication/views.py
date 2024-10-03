from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from .forms import RegistrationForm, UserForm


# Create your views here.
class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    success_url = reverse_lazy('homepage')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')

class ProfileView(LoginRequiredMixin, View):
    template_name = 'register/profile.html'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        password_form = PasswordChangeCustomForm(user=request.user)

        return render(request, self.template_name, {
            'user_form': user_form,
            'password_form': password_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        password_form = PasswordChangeCustomForm(user=request.user, data=request.POST)

        if 'username' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profil został zaktualizowany pomyślnie.')
                return redirect('profile')

        if 'old_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Hasło zostało zmienione pomyślnie.')
                return redirect('profile')
            else:
                messages.error(request, "Wystąpił błąd. Proszę spróbuj ponownie.")

        return render(request, self.template_name, {
            'user_form': user_form,
            'password_form': password_form
        })
