from django import forms
from django.forms import inlineformset_factory
from .models import CoachProfile, CoachPreviousClub, CoachFile


class CoachProfileForm(forms.ModelForm):
    class Meta:
        model = CoachProfile
        fields = [
            "first_name", "last_name", "birth_date", "birth_place", "gender", "nationality",
            "diplomas_certificates", "status", "salary_min", "salary_max",
            "current_club_name", "current_club_country", "current_club_division",
            "current_club_start", "current_club_end",
            "contract_end_date", "achievements",
            "has_agent_contract", "agent_full_name", "agent_id", "represent_self",
            "search_objective", "target_club_notes",
            "visibility_mode", "visibility_filters", "visibility_exceptions",
        ]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "birth_date": "Date de naissance",
            "birth_place": "Lieu de naissance",
            "gender": "Sexe",
            "nationality": "Nationalité",
            "diplomas_certificates": "Diplômes & Certificats",
            "status": "Statut",
            "salary_min": "Salaire minimum",
            "salary_max": "Salaire maximum",
            "current_club_name": "Club actuel",
            "current_club_country": "Pays (club actuel)",
            "current_club_division": "Division (club actuel)",
            "current_club_start": "Date début (club actuel)",
            "current_club_end": "Date fin (club actuel)",
            "contract_end_date": "Date de fin de contrat",
            "achievements": "Réalisations & Palmarès",
            "has_agent_contract": "Contrat avec Agent ?",
            "agent_full_name": "Nom complet de l'agent",
            "agent_id": "ID de l'agent",
            "represent_self": "Voulez-vous vous représenter vous-même ?",
            "search_objective": "Objectif sur la plateforme (Stage, Contrat, Test…)",
            "target_club_notes": "Clubs visés (notes)",
            "visibility_mode": "Préférence de visibilité",
            "visibility_filters": "Filtres de visibilité (JSON)",
            "visibility_exceptions": "Exceptions de visibilité (JSON)",
        }
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "current_club_start": forms.DateInput(attrs={"type": "date"}),
            "current_club_end": forms.DateInput(attrs={"type": "date"}),
            "contract_end_date": forms.DateInput(attrs={"type": "date"}),
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
        }

    def clean(self):
        cleaned = super().clean()
        smin, smax = cleaned.get("salary_min"), cleaned.get("salary_max")
        if smin is not None and smax is not None and smin > smax:
            self.add_error("salary_max", "Le salaire max doit être ≥ salaire min.")
        if cleaned.get("has_agent_contract"):
            if not cleaned.get("agent_full_name") or not cleaned.get("agent_id"):
                self.add_error("agent_full_name", "Nom + ID agent requis si contrat = OUI.")
        return cleaned


PreviousClubFormSet = inlineformset_factory(
    CoachProfile, CoachPreviousClub,
    fields=["club_name", "country", "division", "start_date", "end_date"],
    labels={
        "club_name": "Nom du club",
        "country": "Pays",
        "division": "Division",
        "start_date": "Date de début",
        "end_date": "Date de fin",
    },
    extra=1, can_delete=True,
    widgets={
        "start_date": forms.DateInput(attrs={"type": "date"}),
        "end_date": forms.DateInput(attrs={"type": "date"}),
    }
)

FileFormSet = inlineformset_factory(
    CoachProfile, CoachFile,
    fields=["file_type", "file", "title"],
    labels={
        "file_type": "Type de fichier",
        "file": "Fichier",
        "title": "Titre",
    },
    extra=1, can_delete=True
)
