from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label=_('Użytkownik'),
        help_text=_(
            'Wymagania dla nazwy użytkownika.\nMaksymalnie 150 znaków.\nTylko litery, cyfry i następujące znaki @/./+/-/_.'
        ),
        error_messages={
            'required': _('To pole jest wymagane.'),
            'invalid': _('Wprowadź poprawną nazwę użytkownika.'),
            'unique': _('Użytkownik o takiej nazwie już istnieje.')
        },
    )
    first_name = forms.CharField(
        max_length=150,
        label=_('Imię'),
        error_messages={'required': _('To pole jest wymagane.'),}
    )
    last_name = forms.CharField(
        max_length=150,
        label=_('Nazwisko'),
        error_messages={'required': _('To pole jest wymagane.'),}
    )
    email = forms.EmailField(
        label=_('Email'),
        error_messages={
            'required': _('To pole jest wymagane.'),
            'invalid': _('Wprowadź poprawny adres email.')
        }
    )
    age = forms.IntegerField(
        label=_('Wiek'),
        error_messages={
            'required': _('To pole jest wymagane.'),
            'invalid': _('Wprowadź poprawny wiek.'),
            'min_value': _('Musisz mieć co najmniej 13 lat.')
        }
    )
    password1 = forms.CharField(
        label=_('Hasło'),
        widget=forms.PasswordInput,
        help_text=_(
            "<ul>"
            "<li>Twoje hasło nie może być podobne do twoich innych danych osobowych.</li>"
            "<li>Twoje hasło musi zawierać co najmniej 8 znaków.</li>"
            "<li>Twoje hasło nie może być powszechnie używane.</li>"
            "<li>Twoje hasło nie może składać się wyłącznie z cyfr.</li>"
            "</ul>"
        ),
        error_messages={
            'required': _("To pole jest wymagane."),
            'password_too_short': _("Hasło jest zbyt krótkie. Powinno zawierać co najmniej 8 znaków."),
            'password_common': _("Hasło jest zbyt powszechne."),
            'password_entirely_numeric': _("Hasło nie może być całkowicie numeryczne.")
        }
    )
    password2 = forms.CharField(
        label=_('Potwierdzenie hasła'),
        widget=forms.PasswordInput,
        help_text=_("Wprowadź to samo hasło, co powyżej, w celu jego weryfikacji."),
        error_messages={
            'required': _("To pole jest wymagane."),
            'password_mismatch': _("Hasła nie pasują do siebie.")
        }
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password1', 'password2']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 13:
            raise forms.ValidationError(_("Musisz mieć co najmniej 13 lat."))
        return age

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                validate_password(password1, self.instance)
            except forms.ValidationError as e:
                error_messages = {
                    'password_too_short': self.fields['password1'].error_messages.get('password_too_short', "Hasło jest zbyt krótkie."),
                    'password_too_common': self.fields['password1'].error_messages.get('password_common', "Hasło jest zbyt powszechne."),
                    'password_entirely_numeric': self.fields['password1'].error_messages.get('password_entirely_numeric', "Hasło nie może być całkowicie numeryczne."),
                }
                raise forms.ValidationError([error_messages.get(error.code, str(error)) for error in e.error_list])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.fields['password2'].error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

