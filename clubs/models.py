from django.conf import settings
from django.db import models


class ClubProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="club_profile",
    )

    club_name = models.CharField("Nom du club", max_length=140)
    function = models.CharField(
        "Fonction",
        max_length=80,
        blank=True,
        help_text="Ex: Président, Directeur sportif, Recruteur...",
    )

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.club_name or f"Club #{self.pk}"
