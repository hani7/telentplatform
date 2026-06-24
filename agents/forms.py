from django import forms
from .models import AgentProfile, AgentFile
from django.forms import inlineformset_factory


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
            "agency_role",
            "intervention_countries",
            "covered_markets",
            "represents_mainly",
            "specialties",
            "specialization",
            "years_experience",
            "bio",
            "availability",
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
            "agency_role": "Fonction dans l'agence",
            "intervention_countries": "Pays d'intervention",
            "covered_markets": "Marchés couverts",
            "represents_mainly": "Je représente principalement",
            "specialties": "Spécialités",
            "specialization": "Spécialisation",
            "years_experience": "Années d'expérience",
            "bio": "Biographie professionnelle",
            "availability": "Disponibilité actuelle",
        }
        
        MARKETS_CHOICES = [
            ('National', 'National'),
            ('International', 'International'),
            ('Europe', 'Europe'),
            ('Afrique', 'Afrique'),
            ('Asie', 'Asie'),
            ('Amérique du Nord', 'Amérique du Nord'),
            ('Amérique du Sud', 'Amérique du Sud'),
            ('Moyen-Orient', 'Moyen-Orient'),
        ]
        REPRESENTS_CHOICES = [
            ('Joueurs professionnels', 'Joueurs professionnels'),
            ('Joueurs semi-professionnels', 'Joueurs semi-professionnels'),
            ('Jeunes joueurs', 'Jeunes joueurs'),
            ('Entraîneurs', 'Entraîneurs'),
            ('Clubs', 'Clubs'),
            ('Académies', 'Académies'),
        ]
        SPECIALTIES_CHOICES = [
            ('Négociation de contrats', 'Négociation de contrats'),
            ('Transferts nationaux', 'Transferts nationaux'),
            ('Transferts internationaux', 'Transferts internationaux'),
            ('Développement de carrière', 'Développement de carrière'),
            ('Recherche de clubs', 'Recherche de clubs'),
            ('Gestion d\'image', 'Gestion d\'image'),
            ('Accompagnement des jeunes talents', 'Accompagnement des jeunes talents'),
        ]

        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "license_obtain_date": forms.DateInput(attrs={"type": "date"}),
            "license_expiry_date": forms.DateInput(attrs={"type": "date"}),
            "professional_address": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Votre adresse professionnelle complète"
            }),
            "covered_markets": forms.CheckboxSelectMultiple(choices=MARKETS_CHOICES),
            "represents_mainly": forms.CheckboxSelectMultiple(choices=REPRESENTS_CHOICES),
            "specialties": forms.CheckboxSelectMultiple(choices=SPECIALTIES_CHOICES),
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

class AgentFileForm(forms.ModelForm):
    class Meta:
        model = AgentFile
        fields = ["file", "title"]
        labels = {
            "file": "Fichier (PDF, Image...)",
            "title": "Titre du document",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Ex: CV, Carte pro..."})
        }

AgentFileFormSet = inlineformset_factory(
    AgentProfile,
    AgentFile,
    form=AgentFileForm,
    extra=0,
    can_delete=True
)
