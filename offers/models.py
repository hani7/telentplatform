from django.conf import settings
from django.db import models


class Offer(models.Model):
    class Status(models.TextChoices):
        PENDING  = "PENDING",  "En attente"
        ACCEPTED = "ACCEPTED", "Acceptée"
        DECLINED = "DECLINED", "Refusée"

    class RecipientRole(models.TextChoices):
        PLAYER = "PLAYER", "Joueur"
        COACH  = "COACH",  "Entraîneur"

    sender    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_offers",
        help_text="Agent ou Club qui envoie l'offre"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_offers",
        help_text="Joueur ou Entraîneur qui reçoit l'offre"
    )
    title     = models.CharField(max_length=200)
    message   = models.TextField()
    status    = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.sender} → {self.recipient})"

    def status_css(self):
        return {
            self.Status.PENDING:  "warning",
            self.Status.ACCEPTED: "success",
            self.Status.DECLINED: "danger",
        }.get(self.status, "secondary")
