from django import forms
from django.forms import inlineformset_factory
from .models import PlayerProfile, PlayerPreviousClub, PlayerStat, PlayerFile
from .countries import COUNTRIES


class PlayerProfileForm(forms.ModelForm):
    # Override nationality to use choices directly instead of ForeignKey
    nationality = forms.ChoiceField(
        choices=[('', '-- Sélectionner une nationalité --')] + COUNTRIES,
        required=False,
        label="Nationalité",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    # Override current_club_country to use choices
    current_club_country = forms.ChoiceField(
        choices=[('', '-- Sélectionner un pays --')] + COUNTRIES,
        required=False,
        label="Pays (avec club actuel)"
    )
    
    # Override position to be a dropdown
    position = forms.ChoiceField(
        choices=[
            ('', '-- Sélectionner un poste --'),
            ('Gardien de but', 'Gardien de but'),
            ('Défenseur central', 'Défenseur central'),
            ('Arrière droit', 'Arrière droit'),
            ('Arrière gauche', 'Arrière gauche'),
            ('Piston droit', 'Piston droit'),
            ('Piston gauche', 'Piston gauche'),
            ('Milieu défensif', 'Milieu défensif'),
            ('Milieu central', 'Milieu central'),
            ('Milieu droit', 'Milieu droit'),
            ('Milieu gauche', 'Milieu gauche'),
            ('Milieu offensif', 'Milieu offensif'),
            ('Ailier droit', 'Ailier droit'),
            ('Ailier gauche', 'Ailier gauche'),
            ('Deuxième attaquant', 'Deuxième attaquant'),
            ('Avant-centre / Attaquant', 'Avant-centre / Attaquant'),
        ],
        required=False,
        label="Poste",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    search_objective = forms.ChoiceField(
        choices=[
            ('', '-- Sélectionner --'),
            ('Opportunités sportives', 'Opportunités sportives'),
            ('Contrats', 'Contrats'),
            ('Clubs', 'Clubs'),
            ('Développement', 'Développement'),
            ('Visibilité', 'Visibilité'),
            ('Relance de carrière', 'Relance de carrière'),
            ('Accompagnement', 'Accompagnement'),
        ],
        required=False,
        label="Je cherche...",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    class Meta:
        model = PlayerProfile
        fields = [
            "first_name", "last_name", "birth_date", "birth_place", "gender",
            "is_minor", "parents_declaration", "parents_notes",
            "parent_name", "parent_email", "parent_phone",

            "status", "position", "desired_salary", "foot",
            "height_cm", "weight_kg",

            "availability", "current_club_name", "current_club_country", "current_club_division",
            "current_club_start", "current_club_end",
            "contract_end_date",

            "player_value", "search_objective",

            "has_agent_contract", "agent_full_name", "agent_id", "looking_for_agent", "represent_self",

            "has_transfermarkt", "transfermarkt_username",
            "target_club_notes",
        ]

        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "birth_date": "Date de naissance",
            "birth_place": "Lieu de naissance",
            "gender": "Sexe",
            "nationality": "Nationalité",

            "is_minor": "Joueur mineur ?",
            "parents_declaration": "Déclaration des parents (fichier)",
            "parents_notes": "Renseignements / Notes des parents",
            "parent_name": "Nom et prénom du parent ou tuteur légal",
            "parent_email": "Adresse email",
            "parent_phone": "Téléphone",

            "status": "Statut",
            "position": "Poste",
            "desired_salary": "Salaire souhaité",
            "foot": "Pied",
            "height_cm": "Taille (cm)",
            "weight_kg": "Poids (kg)",

            "availability": "Disponibilité actuelle",
            "current_club_name": "Avec club actuel",
            "current_club_country": "Pays (avec club actuel)",
            "current_club_division": "Division (avec club actuel)",
            "current_club_start": "Date début (avec club actuel)",
            "current_club_end": "Date fin (avec club actuel)",
            "contract_end_date": "Date de fin de contrat",

            "player_value": "Valeur du joueur",
            "search_objective": "Je cherche...",

            "has_agent_contract": "Avez-vous un contrat avec un Agent de Football ?",
            "agent_full_name": "Nom complet de l'agent",
            "agent_id": "ID de l'agent",
            "looking_for_agent": "Cherchez-vous un agent ?",
            "represent_self": "Voulez-vous vous représenter … ?",

            "target_club_notes": "Vous visez quel club ? (notes)",

            "has_transfermarkt": "Avez-vous un profil sur Transfermarkt ?",
            "transfermarkt_username": "Username",
        }

        help_texts = {
            "desired_salary": "Exemple : 1500.00",
            "player_value": "Exemple : 150000.00",
        }

        widgets = {
            # Dates
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "current_club_start": forms.DateInput(attrs={"type": "date"}),
            "current_club_end": forms.DateInput(attrs={"type": "date"}),
            "contract_end_date": forms.DateInput(attrs={"type": "date"}),

            # ✅ Integer
            "height_cm": forms.NumberInput(attrs={"type": "number", "min": 0, "step": 1}),
            "weight_kg": forms.NumberInput(attrs={"type": "number", "min": 0, "step": 1}),

            # ✅ Decimal
            "desired_salary": forms.NumberInput(attrs={"type": "number", "min": 0, "step": "0.01"}),
            "player_value": forms.NumberInput(attrs={"type": "number", "min": 0, "step": "0.01"}),

            # Textareas
            "parents_notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Infos utiles (optionnel)"}),
            "target_club_notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Ex: clubs souhaités, pays, division…"}),

            "parent_email": forms.EmailInput(attrs={"type": "email", "placeholder": "Email du parent/tuteur"}),
            "parent_phone": forms.TextInput(attrs={"type": "tel", "placeholder": "Téléphone du parent/tuteur"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bool_choices = [(True, 'Oui'), (False, 'Non')]
        for field in ['has_agent_contract', 'looking_for_agent', 'has_transfermarkt', 'represent_self']:
            self.fields[field].widget = forms.Select(choices=[('', '---------')] + bool_choices, attrs={"class": "form-control"})
            self.fields[field].required = False

    def clean(self):
        cleaned = super().clean()

        if cleaned.get("has_transfermarkt"):
            if not cleaned.get("transfermarkt_username"):
                self.add_error("transfermarkt_username", "Veuillez renseigner votre username Transfermarkt.")
        else:
            cleaned["transfermarkt_username"] = ""

        if cleaned.get("has_agent_contract"):
            if not cleaned.get("agent_full_name") or not cleaned.get("agent_id"):
                self.add_error("agent_full_name", "Veuillez renseigner le nom et l’ID de l’agent (contrat = OUI).")
                self.add_error("agent_id", "Veuillez renseigner l’ID de l’agent (contrat = OUI).")
            cleaned["looking_for_agent"] = False
        else:
            cleaned["agent_full_name"] = ""
            cleaned["agent_id"] = ""

        if cleaned.get("is_minor"):
            if not cleaned.get("parents_declaration"):
                self.add_error("parents_declaration", "La déclaration des parents est obligatoire si le joueur est mineur.")
            if not cleaned.get("parent_name"):
                self.add_error("parent_name", "Le nom et prénom du parent ou tuteur légal est obligatoire.")
            if not cleaned.get("parent_email"):
                self.add_error("parent_email", "L'adresse email du parent ou tuteur légal est obligatoire.")
            if not cleaned.get("parent_phone"):
                self.add_error("parent_phone", "Le numéro de téléphone du parent ou tuteur légal est obligatoire.")

        if cleaned.get("availability") == "FREE":
            cleaned["current_club_name"] = ""
            cleaned["current_club_country"] = ""
            cleaned["current_club_division"] = ""
            cleaned["current_club_start"] = None
            cleaned["current_club_end"] = None

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convert nationality string to Nationality instance
        nationality_name = self.cleaned_data.get('nationality')
        if nationality_name:
            from .models import Nationality
            nationality_obj, created = Nationality.objects.get_or_create(name=nationality_name)
            instance.nationality = nationality_obj
        else:
            instance.nationality = None
        
        if commit:
            instance.save()
        return instance


# --------- Formset : Clubs précédents ---------
class PreviousClubForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=[('', '-- Sélectionner un pays --')] + COUNTRIES,
        required=False,
        label="Pays"
    )
    
    class Meta:
        model = PlayerPreviousClub
        fields = ["club_name", "country", "division", "season"]
        labels = {
            "club_name": "Nom du club",
            "division": "Division",
            "season": "Saison",
        }
        widgets = {
            "season": forms.TextInput(attrs={"placeholder": "Ex: 2023-2024"}),
        }

PreviousClubFormSet = inlineformset_factory(
    PlayerProfile,
    PlayerPreviousClub,
    form=PreviousClubForm,
    extra=1,
    can_delete=True,
)

# --------- Formset : Saisons/Stats par Club ---------
COMPETITION_CHOICES = [
    ('championnat', 'Championnat'),
    ('coupe_nationale', 'Coupe nationale'),
    ('coupe_regionale', 'Coupe régionale'),
    ('ligue_champions', 'Ligue des champions continentale'),
    ('tournoi_international', 'Tournoi international'),
    ('matchs_amicaux', 'Matchs amicaux'),
    ('autre_competition', 'Autre'),
]

COLLECTIVE_RESULT_CHOICES = [
    ('champion', 'Champion'),
    ('vice_champion', 'Vice-champion'),
    ('promotion', 'Promotion'),
    ('maintien', 'Maintien'),
    ('qualification_continentale', 'Qualification continentale'),
    ('vainqueur_coupe', 'Vainqueur de coupe'),
    ('relegation', 'Relégation'),
    ('autre_resultat', 'Autre'),
]

class SeasonStatForm(forms.ModelForm):
    competitions = forms.MultipleChoiceField(
        choices=COMPETITION_CHOICES,
        required=False,
        label="Compétitions disputées",
        widget=forms.CheckboxSelectMultiple()
    )
    collective_results = forms.MultipleChoiceField(
        choices=COLLECTIVE_RESULT_CHOICES,
        required=False,
        label="Résultats collectifs",
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = PlayerStat
        fields = ["season", "matches", "goals", "assists", "minutes", "competitions", "collective_results"]
        labels = {
            "season": "Saison",
            "matches": "Matchs",
            "goals": "Buts",
            "assists": "Passes D",
            "minutes": "Minutes",
        }
        widgets = {
            "season": forms.TextInput(attrs={"placeholder": "Ex: 2023-2024"}),
            "matches": forms.NumberInput(attrs={"min": 0, "step": 1, "placeholder": "0"}),
            "goals": forms.NumberInput(attrs={"min": 0, "step": 1, "placeholder": "0"}),
            "assists": forms.NumberInput(attrs={"min": 0, "step": 1, "placeholder": "0"}),
            "minutes": forms.NumberInput(attrs={"min": 0, "step": 1, "placeholder": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate multi-choice fields from JSON
        if self.instance.pk:
            self.initial['competitions'] = self.instance.competitions or []
            self.initial['collective_results'] = self.instance.collective_results or []

    def clean_competitions(self):
        return self.cleaned_data.get('competitions', [])

    def clean_collective_results(self):
        return self.cleaned_data.get('collective_results', [])

SeasonStatFormSet = inlineformset_factory(
    PlayerPreviousClub,
    PlayerStat,
    form=SeasonStatForm,
    extra=1,
    can_delete=True,
)


# --------- Formset : Fichiers ---------
FileFormSet = inlineformset_factory(
    PlayerProfile,
    PlayerFile,
    fields=["file_type", "file", "title"],
    extra=1,
    can_delete=True
)
