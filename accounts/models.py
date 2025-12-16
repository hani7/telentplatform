from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        PLAYER = "PLAYER", "Joueur"
        COACH  = "COACH", "Entraîneur"
        AGENT  = "AGENT", "Agent"
        CLUB   = "CLUB", "Club"

    role = models.CharField(max_length=10, choices=Role.choices)
    phone = models.CharField(max_length=30, blank=True)
