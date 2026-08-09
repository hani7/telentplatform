from django import forms
from django.forms import inlineformset_factory
from .models import CoachProfile, CoachPreviousClub, CoachFile, CoachStat
from players.countries import COUNTRIES


class CoachProfileForm(forms.ModelForm):
    nationality = forms.ChoiceField(
        choices=[('', '-- Sélectionner une nationalité --')] + COUNTRIES,
        required=True,
        label="Nationalité",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    current_club_country = forms.ChoiceField(
        choices=[('', '-- Sélectionner un pays --')] + COUNTRIES,
        required=False,
        label="Pays"
    )

    currency = forms.ChoiceField(
        choices=[
            ('EUR', 'Euro (EUR)'),
            ('USD', 'Dollar Américain (USD)'),
            ('GBP', 'Livre Sterling (GBP)'),
            ('DZD', 'Dinar Algérien (DZD)'),
            ('MAD', 'Dirham Marocain (MAD)'),
            ('TND', 'Dinar Tunisien (TND)'),
            ('XOF', 'Franc CFA (XOF)'),
            ('XAF', 'Franc CFA (XAF)'),
            ('ZAR', 'Rand Sud-Africain (ZAR)'),
            ('CHF', 'Franc Suisse (CHF)'),
            ('CAD', 'Dollar Canadien (CAD)'),
            ('AUD', 'Dollar Australien (AUD)'),
            ('JPY', 'Yen Japonais (JPY)'),
            ('CNY', 'Yuan Chinois (CNY)'),
            ('INR', 'Roupie Indienne (INR)'),
            ('BRL', 'Réal Brésilien (BRL)'),
            ('MXN', 'Peso Mexicain (MXN)'),
            ('RUB', 'Rouble Russe (RUB)'),
            ('TRY', 'Livre Turque (TRY)'),
            ('NGN', 'Naira Nigérian (NGN)'),
            ('EGP', 'Livre Égyptienne (EGP)'),
            ('SEK', 'Couronne Suédoise (SEK)'),
            ('NOK', 'Couronne Norvégienne (NOK)'),
            ('DKK', 'Couronne Danoise (DKK)'),
            ('PLN', 'Zloty Polonais (PLN)'),
            ('OTHER', 'Autre devise')
        ],
        required=False,
        label="Devise",
        widget=forms.Select()
    )

    search_objective = forms.ChoiceField(
        choices=[
            ('', '-- Sélectionner --'),
            ('Opportunités sportives', 'Opportunités sportives'),
            ('Contrats', 'Contrats'),
            ('Clubs', 'Clubs'),
            ('Développement', 'Développement'),
            ('Visibilité', 'Visibilité'),
        ],
        required=False,
        label="Je cherche...",
        widget=forms.Select()
    )

    class Meta:
        model = CoachProfile
        fields = [
            "first_name", "last_name", "birth_date", "birth_place", "gender", "nationality", "profile_photo",
            "diplomas_certificates", "status", "availability", "salary_min", "salary_max", "currency",
            "current_club_name", "current_club_country", "current_club_division",
            "current_club_start", "current_club_end", "achievements",
            "has_agent_contract", "agent_full_name", "agent_id", "looking_for_agent",
            "agent_contract_start", "agent_contract_end",
            "has_transfermarkt", "transfermarkt_username",
            "search_objective", "target_club_notes",
            "visibility_filters", "visibility_exceptions",
            "is_minor", "parent_name", "parent_relation", "parent_relation_other",
            "parent_birth_date", "parent_nationality", "parent_address",
            "parent_phone", "parent_email", "parents_notes"
        ]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "birth_date": "Date de naissance",
            "birth_place": "Lieu de naissance",
            "gender": "Sexe",
            "nationality": "Nationalité",
            "profile_photo": "Photo de profil",
            "diplomas_certificates": "Diplômes & Certificats",
            "status": "Statut",
            "availability": "Disponibilité actuelle",
            "salary_min": "Salaire minimum",
            "salary_max": "Salaire maximum",
            "current_club_name": "Club actuel",
            "current_club_country": "Pays",
            "current_club_division": "Division",
            "current_club_start": "Date début",
            "current_club_end": "Date fin",
            "achievements": "Réalisations & Palmarès",
            "has_agent_contract": "Contrat avec un Agent ?",
            "agent_full_name": "Nom complet",
            "agent_id": "ID",
            "agent_contract_start": "Date début",
            "agent_contract_end": "Date fin",
            "looking_for_agent": "Cherchez-vous un agent ?",
            "search_objective": "Je cherche...",
            "target_club_notes": "Clubs visés (notes)",
            "has_transfermarkt": "Avez-vous un profil sur Transfermarkt ?",
            "transfermarkt_username": "Username ou lien",
            "visibility_filters": "Filtres de visibilité (JSON)",
            "visibility_exceptions": "Exceptions de visibilité (JSON)",
            "is_minor": "Je suis mineur",
            "parent_name": "Nom complet du représentant légal",
            "parent_relation": "Lien de parenté",
            "parent_relation_other": "Précisez (Autre)",
            "parent_birth_date": "Date de naissance du représentant",
            "parent_nationality": "Nationalité du représentant",
            "parent_address": "Adresse complète du représentant",
            "parent_phone": "Téléphone du représentant",
            "parent_email": "Email du représentant",
            "parents_notes": "Remarques (optionnel)",
        }
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "current_club_name": forms.TextInput(attrs={"autocomplete": "off", "placeholder": "Tapez le nom du club..."}),
            "current_club_start": forms.DateInput(attrs={"type": "date"}),
            "current_club_end": forms.DateInput(attrs={"type": "date"}),
            "agent_contract_start": forms.DateInput(attrs={"type": "date"}),
            "agent_contract_end": forms.DateInput(attrs={"type": "date"}),
            "diplomas_certificates": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Ex: CAF-A, UEFA-Pro, Licence nationale..."
            }),
            "achievements": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Ex: Champion de Ligue 1 2022, Coupe d'Algérie 2021..."
            }),
            "target_club_notes": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Ex: clubs souhaités, pays, division…"
            }),
            "visibility_filters": forms.Textarea(attrs={"rows": 2}),
            "visibility_exceptions": forms.Textarea(attrs={"rows": 2}),
            "availability": forms.Select(attrs={"data-sd-skip": "1"}),
            "parent_relation": forms.Select(attrs={"data-sd-skip": "1"}),
            "parent_birth_date": forms.DateInput(attrs={"type": "date"}),
            "parents_notes": forms.Textarea(attrs={"rows": 3}),
            "is_minor": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bool_choices = [(True, 'Oui'), (False, 'Non')]
        for field in ['has_agent_contract', 'looking_for_agent', 'has_transfermarkt']:
            self.fields[field].widget = forms.Select(choices=[('', '---------')] + bool_choices, attrs={"class": "form-control"})
            self.fields[field].required = False
        
        self.fields['nationality'].required = True

    def clean(self):
        cleaned = super().clean()
        smin, smax = cleaned.get("salary_min"), cleaned.get("salary_max")
        if smin is not None and smax is not None and smin > smax:
            self.add_error("salary_max", "Le salaire max doit être ≥ salaire min.")
        if cleaned.get("has_agent_contract"):
            if not cleaned.get("agent_full_name") or not cleaned.get("agent_id"):
                self.add_error("agent_full_name", "Nom + ID agent requis si contrat = OUI.")
            cleaned["looking_for_agent"] = False
        else:
            cleaned["agent_full_name"] = ""
            cleaned["agent_id"] = ""
                
        if cleaned.get("has_transfermarkt"):
            if not cleaned.get("transfermarkt_username"):
                self.add_error("transfermarkt_username", "Veuillez renseigner votre username ou lien Transfermarkt.")
        else:
            cleaned["transfermarkt_username"] = ""

        if cleaned.get("availability") == "FREE":
            cleaned["current_club_name"] = ""
            cleaned["current_club_country"] = ""
            cleaned["current_club_division"] = ""
            cleaned["current_club_start"] = None
            cleaned["current_club_end"] = None
            
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        from players.models import Nationality
        
        nationality_name = self.cleaned_data.get('nationality')
        if nationality_name:
            nationality_obj, _ = Nationality.objects.get_or_create(name=nationality_name)
            instance.nationality = nationality_obj
        else:
            instance.nationality = None

        if commit:
            instance.save()
        return instance


class CoachPreviousClubForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=[('', '-- Sélectionner un pays --')] + COUNTRIES,
        required=False,
        label="Pays"
    )
    
    class Meta:
        model = CoachPreviousClub
        fields = ["club_name", "country", "division", "start_date", "end_date"]
        labels = {
            "club_name": "Nom du club",
            "division": "Division",
            "start_date": "Date de début",
            "end_date": "Date de fin",
        }
        widgets = {
            "club_name": forms.TextInput(attrs={"autocomplete": "off", "placeholder": "Tapez le nom du club..."}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

PreviousClubFormSet = inlineformset_factory(
    CoachProfile, CoachPreviousClub,
    form=CoachPreviousClubForm,
    extra=1, can_delete=True,
)

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

class CoachSeasonStatForm(forms.ModelForm):
    competitions = forms.MultipleChoiceField(
        choices=COMPETITION_CHOICES,
        required=False,
        label="Compétitions disputées",
        widget=forms.CheckboxSelectMultiple()
    )
    competitions_other = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Précisez l'autre compétition...", "style": "display:none;", "class": "form-control"})
    )
    collective_results = forms.MultipleChoiceField(
        choices=COLLECTIVE_RESULT_CHOICES,
        required=False,
        label="Résultats collectifs",
        widget=forms.CheckboxSelectMultiple()
    )
    collective_results_other = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Précisez l'autre résultat...", "style": "display:none;", "class": "form-control"})
    )

    class Meta:
        model = CoachStat
        fields = ["season", "competitions", "competitions_other", "collective_results", "collective_results_other"]
        labels = {
            "season": "Saison",
        }
        widgets = {
            "season": forms.TextInput(attrs={"placeholder": "Ex: 2023-2024"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['competitions'] = self.instance.competitions or []
            self.initial['collective_results'] = self.instance.collective_results or []

    def clean_competitions(self):
        return self.cleaned_data.get('competitions', [])

    def clean_collective_results(self):
        return self.cleaned_data.get('collective_results', [])

SeasonStatFormSet = inlineformset_factory(
    CoachPreviousClub, CoachStat,
    form=CoachSeasonStatForm,
    extra=1, can_delete=True,
)

FileFormSet = inlineformset_factory(
    CoachProfile, CoachFile,
    fields=["file_type", "file"],
    labels={
        "file_type": "Type de fichier",
        "file": "Fichier",
        "title": "Titre",
    },
    extra=1, can_delete=True
)
