from django import forms
from django.forms import inlineformset_factory
from .models import PlayerProfile, PlayerPreviousClub, PlayerStat, PlayerFile


class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = [
            "first_name", "last_name", "birth_date", "birth_place", "gender", "nationality",
            "is_minor", "parents_declaration", "parents_notes",

            "status", "position", "salary_min", "salary_max", "foot",
            "height_cm", "weight_kg",

            "current_club_name", "current_club_country", "current_club_division",
            "current_club_start", "current_club_end",
            "contract_end_date",

            "player_value", "search_objective",

            "has_agent_contract", "agent_full_name", "agent_id", "represent_self",

            "target_club_notes", "visibility_mode", "visibility_filters", "visibility_exceptions",
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

            "status": "Statut",
            "position": "Poste",
            "salary_min": "Salaire minimum",
            "salary_max": "Salaire maximum",
            "foot": "Pied",
            "height_cm": "Taille (cm)",
            "weight_kg": "Poids (kg)",

            "current_club_name": "Club actuel",
            "current_club_country": "Pays (club actuel)",
            "current_club_division": "Division (club actuel)",
            "current_club_start": "Date début (club actuel)",
            "current_club_end": "Date fin (club actuel)",
            "contract_end_date": "Date de fin de contrat",

            "player_value": "Valeur du joueur",
            "search_objective": "Que cherchez-vous sur la plateforme ? (Stage, Test, Contrat…)",

            "has_agent_contract": "Contrat avec Agent ?",
            "agent_full_name": "Nom complet de l’agent",
            "agent_id": "ID de l’agent",
            "represent_self": "Voulez-vous vous représenter vous-même ?",

            "target_club_notes": "Vous visez quel club ? (notes)",
            "visibility_mode": "Préférence de visibilité",
            "visibility_filters": "Filtres de visibilité (JSON)",
            "visibility_exceptions": "Exceptions de visibilité (JSON)",
        }

        help_texts = {
            "salary_min": "Exemple : 1000.00",
            "salary_max": "Exemple : 2000.00",
            "player_value": "Exemple : 150000.00",
            "visibility_filters": 'Exemple : {"countries":["DZ"],"divisions":[],"clubs":[]}',
            "visibility_exceptions": 'Exemple : {"countries":[],"divisions":[],"clubs":["Club X"]}',
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
            "salary_min": forms.NumberInput(attrs={"type": "number", "min": 0, "step": "0.01"}),
            "salary_max": forms.NumberInput(attrs={"type": "number", "min": 0, "step": "0.01"}),
            "player_value": forms.NumberInput(attrs={"type": "number", "min": 0, "step": "0.01"}),

            # Textareas
            "parents_notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Infos utiles (optionnel)"}),
            "target_club_notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Ex: clubs souhaités, pays, division…"}),
            "visibility_filters": forms.Textarea(attrs={"rows": 2}),
            "visibility_exceptions": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned = super().clean()

        salaire_min = cleaned.get("salary_min")
        salaire_max = cleaned.get("salary_max")

        if salaire_min is not None and salaire_max is not None and salaire_min > salaire_max:
            self.add_error("salary_max", "Le salaire maximum doit être supérieur ou égal au salaire minimum.")

        if cleaned.get("has_agent_contract"):
            if not cleaned.get("agent_full_name") or not cleaned.get("agent_id"):
                self.add_error("agent_full_name", "Veuillez renseigner le nom et l’ID de l’agent (contrat = OUI).")
                self.add_error("agent_id", "Veuillez renseigner l’ID de l’agent (contrat = OUI).")

        if cleaned.get("is_minor") and not cleaned.get("parents_declaration"):
            self.add_error("parents_declaration", "La déclaration des parents est obligatoire si le joueur est mineur.")

        return cleaned


# --------- Formset : Clubs précédents ---------
PreviousClubFormSet = inlineformset_factory(
    PlayerProfile,
    PlayerPreviousClub,
    fields=["club_name", "country", "division", "start_date", "end_date"],
    extra=1,
    can_delete=True,
    widgets={
        "start_date": forms.DateInput(attrs={"type": "date"}),
        "end_date": forms.DateInput(attrs={"type": "date"}),
    }
)


# --------- Formset : Stats (champs integer) ---------
StatFormSet = inlineformset_factory(
    PlayerProfile,
    PlayerStat,
    fields=["season", "matches", "goals", "assists", "minutes"],
    extra=1,
    can_delete=True,
    widgets={
        "matches": forms.NumberInput(attrs={"type": "number", "min": 0, "step": 1}),
        "goals": forms.NumberInput(attrs={"type": "number", "min": 0, "step": 1}),
        "assists": forms.NumberInput(attrs={"type": "number", "min": 0, "step": 1}),
        "minutes": forms.NumberInput(attrs={"type": "number", "min": 0, "step": 1}),
    }
)


# --------- Formset : Fichiers ---------
FileFormSet = inlineformset_factory(
    PlayerProfile,
    PlayerFile,
    fields=["file_type", "file", "title"],
    extra=1,
    can_delete=True
)
