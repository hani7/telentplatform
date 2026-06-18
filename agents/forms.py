from django import forms
from .models import AgentProfile


class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "birth_place",
            "gender",
            "nationality",
            "license_number",
            "agency_name",
            "specialization",
            "years_experience",
            "bio",
        ]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "birth_date": "Date de naissance",
            "birth_place": "Lieu de naissance",
            "gender": "Sexe",
            "nationality": "Nationalité",
            "license_number": "Numéro de licence (FIFA / fédérale)",
            "agency_name": "Nom de l'agence",
            "specialization": "Spécialisation",
            "years_experience": "Années d'expérience",
            "bio": "Biographie",
        }
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Parlez de vous, votre expérience, vos spécialités..."
            }),
            "specialization": forms.TextInput(attrs={
                "placeholder": "Ex: Joueurs offensifs, Ligue 1 algérienne..."
            }),
            "license_number": forms.TextInput(attrs={
                "placeholder": "Ex: FIFA-2024-DZ-001"
            }),
            "agency_name": forms.TextInput(attrs={
                "placeholder": "Ex: Elite Football Agency"
            }),
        }
