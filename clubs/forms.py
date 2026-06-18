from django import forms
from .models import ClubProfile


class ClubProfileForm(forms.ModelForm):
    class Meta:
        model = ClubProfile
        fields = ["club_name", "function"]
        widgets = {
            "club_name": forms.TextInput(attrs={"placeholder": "Nom du club"}),
            "function": forms.TextInput(attrs={"placeholder": "Ex: Président, Directeur sportif..."}),
        }
