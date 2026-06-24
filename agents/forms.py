from django import forms
from .models import AgentProfile


class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = [
            "first_name",
            "last_name",
            "profile_photo",
            "birth_date",
            "birth_place",
            "gender",
            "nationality",
            "country_city",
            "professional_address",
            "contact_email",
            "mobile_phone",
            "professional_phone",
            "website",
            "social_media",
            "license_number",
            "federation",
            "license_status",
            "license_obtain_date",
            "license_expiry_date",
            "agency_name",
            "specialization",
            "years_experience",
            "bio",
        ]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "profile_photo": "Photo de profil",
            "birth_date": "Date de naissance",
            "birth_place": "Lieu de naissance",
            "gender": "Sexe",
            "nationality": "Nationalité",
            "country_city": "Pays / ville",
            "professional_address": "Adresse professionnelle",
            "contact_email": "E-mail de contact",
            "mobile_phone": "Téléphone mobile",
            "professional_phone": "Téléphone professionnel",
            "website": "Site web",
            "social_media": "Réseaux sociaux professionnels",
            "license_number": "Numéro de licence",
            "federation": "Fédération / association de rattachement",
            "license_status": "Statut de la licence",
            "license_obtain_date": "Date d'obtention de la licence",
            "license_expiry_date": "Date d'échéance (si applicable)",
            "agency_name": "Nom de l'agence",
            "specialization": "Spécialisation",
            "years_experience": "Années d'expérience",
            "bio": "Biographie",
        }
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "license_obtain_date": forms.DateInput(attrs={"type": "date"}),
            "license_expiry_date": forms.DateInput(attrs={"type": "date"}),
            "professional_address": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Votre adresse professionnelle complète"
            }),
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
            "social_media": forms.TextInput(attrs={
                "placeholder": "Lien LinkedIn, Twitter, etc."
            }),
            "website": forms.URLInput(attrs={
                "placeholder": "https://www.votre-agence.com"
            }),
        }
