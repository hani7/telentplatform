from django.conf import settings
from django.db import models
from datetime import date
from players.models import Nationality


class AgentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agent_profile",
    )

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=120, blank=True)

    class Gender(models.TextChoices):
        MALE = "M", "Masculin"
        FEMALE = "F", "Féminin"

    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)

    nationality = models.ForeignKey(
        Nationality, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Nouveaux champs d'Identification
    profile_photo = models.FileField(upload_to="agents/photos/", null=True, blank=True)
    country_city = models.CharField(max_length=150, blank=True)
    professional_address = models.TextField(blank=True)

    # Champs de Contact
    contact_email = models.EmailField(blank=True)
    mobile_phone = models.CharField(max_length=50, blank=True)
    professional_phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    social_media = models.CharField(max_length=255, blank=True)

    # Removed duplicated nationality

    license_number = models.CharField(
        max_length=80,
        blank=True,
        help_text="Numéro de licence FIFA / fédérale",
    )
    
    # Nouveaux champs Statut d'agent
    federation = models.CharField(max_length=150, blank=True)
    
    class LicenseStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Actif"
        SUSPENDED = "SUSPENDED", "Suspendu"
        RENEWING = "RENEWING", "En renouvellement"
        
    license_status = models.CharField(max_length=20, choices=LicenseStatus.choices, blank=True)
    license_obtain_date = models.DateField(null=True, blank=True)
    license_expiry_date = models.DateField(null=True, blank=True)

    agency_name = models.CharField(max_length=140, blank=True)
    agency_role = models.CharField(max_length=140, blank=True)
    intervention_countries = models.CharField(max_length=255, blank=True)
    
    # JSON Fields for multi-select
    covered_markets = models.JSONField(default=list, blank=True)
    represents_mainly = models.JSONField(default=list, blank=True)
    specialties = models.JSONField(default=list, blank=True)

    class Specialization(models.TextChoices):
        PLAYERS = "PLAYERS", "Joueurs"
        COACHES = "COACHES", "Entraîneurs"
        BOTH = "BOTH", "Joueurs & Entraîneurs"

    specialization = models.CharField(
        max_length=10,
        choices=Specialization.choices,
        default=Specialization.BOTH,
    )

    years_experience = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    
    class Availability(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponible pour de nouveaux mandats"
        LIMITED = "LIMITED", "Disponibilité limitée"
        UNAVAILABLE = "UNAVAILABLE", "Non disponible actuellement"
        
    availability = models.CharField(max_length=20, choices=Availability.choices, blank=True)

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def is_complete_for_activation(self) -> bool:
        required = [self.first_name, self.last_name, self.license_number]
        return not any(not x for x in required)


class AgentFile(models.Model):
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="agents/files/")
    title = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
