from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
from players.models import Nationality

class CoachProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coach_profile")

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=120, blank=True)

    class Gender(models.TextChoices):
        MALE = "M", "Masculin"
        FEMALE = "F", "Féminin"
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)

    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)

    diplomas_certificates = models.TextField(blank=True)

    class Status(models.TextChoices):
        AMATEUR = "AMATEUR", "Amateur"
        PRO = "PRO", "Pro"
    status = models.CharField(max_length=10, choices=Status.choices, blank=True)

    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    current_club_name = models.CharField(max_length=140, blank=True)
    current_club_country = models.CharField(max_length=80, blank=True)
    current_club_division = models.CharField(max_length=80, blank=True)
    current_club_start = models.DateField(null=True, blank=True)
    current_club_end = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)

    achievements = models.TextField(blank=True)

    has_agent_contract = models.BooleanField(default=False)
    agent_full_name = models.CharField(max_length=140, blank=True)
    agent_id = models.CharField(max_length=50, blank=True)

    represent_self = models.BooleanField(default=True)

    search_objective = models.CharField(max_length=120, blank=True)
    target_club_notes = models.TextField(blank=True)

    class VisibilityMode(models.TextChoices):
        ALL = "ALL", "Pour tout le monde"
        ALL_EXCEPT = "ALL_EXCEPT", "Pour tout le monde sauf"
        SOME = "SOME", "Pour quelques clubs"

    visibility_mode = models.CharField(max_length=15, choices=VisibilityMode.choices, default=VisibilityMode.ALL)
    visibility_filters = models.JSONField(default=dict, blank=True)
    visibility_exceptions = models.JSONField(default=dict, blank=True)

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def is_complete_for_activation(self) -> bool:
        required = [self.first_name, self.last_name, self.birth_date, self.status]
        return not any(not x for x in required)

class CoachPreviousClub(models.Model):
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name="previous_clubs")
    club_name = models.CharField(max_length=140)
    country = models.CharField(max_length=80, blank=True)
    division = models.CharField(max_length=80, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

class CoachFile(models.Model):
    class FileType(models.TextChoices):
        CV = "CV", "CV (PDF)"
        PHOTO = "PHOTO", "Photo"
        VIDEO = "VIDEO", "Vidéo"
        OTHER = "OTHER", "Autre"

    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name="files")
    file_type = models.CharField(max_length=10, choices=FileType.choices)
    file = models.FileField(upload_to="coaches/files/")
    title = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
