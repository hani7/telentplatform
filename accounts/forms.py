from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class LoginForm(AuthenticationForm):
    pass

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
