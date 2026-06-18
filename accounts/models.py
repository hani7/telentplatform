import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        PLAYER = "PLAYER", "Joueur"
        COACH  = "COACH", "Entraîneur"
        AGENT  = "AGENT", "Agent"
        CLUB   = "CLUB", "Club"

    role = models.CharField(max_length=10, choices=Role.choices)
    phone = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)


class OTPCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp_codes")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    @classmethod
    def generate_for(cls, user):
        """Invalidate all previous codes and create a fresh one."""
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        code = f"{random.randint(0, 999999):06d}"
        return cls.objects.create(user=user, code=code)

    def __str__(self):
        return f"OTP {self.code} for {self.user.username}"
