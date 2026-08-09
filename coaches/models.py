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
    profile_photo = models.ImageField(upload_to='coaches/avatars/', null=True, blank=True)

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

    class Availability(models.TextChoices):
        IN_CLUB = "IN_CLUB", "En poste"
        FREE = "FREE", "Libre"
    availability = models.CharField(max_length=15, choices=Availability.choices, blank=True)

    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, blank=True, null=True, default='EUR')

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
    agent_contract_start = models.DateField(null=True, blank=True)
    agent_contract_end = models.DateField(null=True, blank=True)

    looking_for_agent = models.BooleanField(default=False)

    has_transfermarkt = models.BooleanField(default=False)
    transfermarkt_username = models.CharField(max_length=150, blank=True)

    search_objective = models.CharField(max_length=120, blank=True)
    target_club_notes = models.TextField(blank=True)

    is_minor = models.BooleanField(default=False)
    parents_declaration = models.FileField(upload_to="coaches/parents/", null=True, blank=True)
    parents_notes = models.TextField(blank=True)
    
    parent_name = models.CharField(max_length=140, blank=True)
    
    class ParentRelation(models.TextChoices):
        PERE = "PERE", "Père"
        MERE = "MERE", "Mère"
        TUTEUR = "TUTEUR", "Tuteur légal"
        AUTRE = "AUTRE", "Autre"
        
    parent_relation = models.CharField(max_length=15, choices=ParentRelation.choices, blank=True)
    parent_relation_other = models.CharField(max_length=80, blank=True)
    parent_birth_date = models.DateField(null=True, blank=True)
    parent_nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True, related_name="coach_parent_profiles")
    parent_address = models.CharField(max_length=255, blank=True)
    
    parent_email = models.EmailField(blank=True)
    parent_phone = models.CharField(max_length=50, blank=True)

    class ProfileStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Actif"
        PENDING_CONSENT = "PENDING_CONSENT", "En cours de validation"
    profile_status = models.CharField(max_length=20, choices=ProfileStatus.choices, default=ProfileStatus.ACTIVE)
    consent_token = models.UUIDField(null=True, blank=True)

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

class CoachStat(models.Model):
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name="stats")
    club = models.ForeignKey('CoachPreviousClub', on_delete=models.CASCADE, null=True, blank=True, related_name="seasons")
    season = models.CharField(max_length=20, blank=True)
    competitions = models.JSONField(default=list, blank=True)
    competitions_other = models.TextField(blank=True)
    collective_results = models.JSONField(default=list, blank=True)
    collective_results_other = models.TextField(blank=True)

class CoachFile(models.Model):
    class FileType(models.TextChoices):
        CV = "CV", "CV (PDF)"
        PHOTO = "PHOTO", "Photo"
        PROFILE_PHOTO = "PROFILE_PHOTO", "Photo de profil"
        VIDEO = "VIDEO", "Vidéo"
        OTHER = "OTHER", "Autre"

    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name="files")
    file_type = models.CharField(max_length=20, choices=FileType.choices)
    file = models.FileField(upload_to="coaches/files/")
    title = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
