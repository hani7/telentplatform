from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User


class LoginForm(AuthenticationForm):
    """
    Login form that accepts username, email, or phone number.
    The single `username` field is relabelled as 'Identifiant' and
    the FlexibleAuthBackend resolves which field it matches.
    """
    username = forms.CharField(
        label="Identifiant",
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "autocomplete": "username",
            "placeholder": "Nom d'utilisateur, email ou téléphone",
        }),
    )

    error_messages = {
        "invalid_login": (
            "Identifiants incorrects. Vérifiez votre nom d'utilisateur / "
            "email / téléphone et votre mot de passe."
        ),
        "inactive": "Ce compte est désactivé.",
    }

class BaseRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "first_name", "last_name"]

    def save(self, commit=True, role=None):
        user = super().save(commit=False)
        if role:
            user.role = role
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
