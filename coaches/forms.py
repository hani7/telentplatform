from django import forms
from django.forms import inlineformset_factory
from .models import CoachProfile, CoachPreviousClub, CoachFile

class CoachProfileForm(forms.ModelForm):
    class Meta:
        model = CoachProfile
        fields = [
            "first_name","last_name","birth_date","birth_place","gender","nationality",
            "diplomas_certificates","status","salary_min","salary_max",
            "current_club_name","current_club_country","current_club_division","current_club_start","current_club_end",
            "contract_end_date","achievements",
            "has_agent_contract","agent_full_name","agent_id","represent_self",
            "search_objective","target_club_notes",
            "visibility_mode","visibility_filters","visibility_exceptions",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type":"date"}),
            "current_club_start": forms.DateInput(attrs={"type":"date"}),
            "current_club_end": forms.DateInput(attrs={"type":"date"}),
            "contract_end_date": forms.DateInput(attrs={"type":"date"}),
            "diplomas_certificates": forms.Textarea(attrs={"rows":3}),
            "achievements": forms.Textarea(attrs={"rows":3}),
            "target_club_notes": forms.Textarea(attrs={"rows":2}),
            "visibility_filters": forms.Textarea(attrs={"rows":2}),
            "visibility_exceptions": forms.Textarea(attrs={"rows":2}),
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
    fields=["club_name","country","division","start_date","end_date"],
    extra=1, can_delete=True,
    widgets={
        "start_date": forms.DateInput(attrs={"type":"date"}),
        "end_date": forms.DateInput(attrs={"type":"date"}),
    }
)

FileFormSet = inlineformset_factory(
    CoachProfile, CoachFile,
    fields=["file_type","file","title"],
    extra=1, can_delete=True
)
