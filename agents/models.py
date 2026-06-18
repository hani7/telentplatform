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

    license_number = models.CharField(
        max_length=80,
        blank=True,
        help_text="Numéro de licence FIFA / fédérale",
    )
    agency_name = models.CharField(max_length=140, blank=True)

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
