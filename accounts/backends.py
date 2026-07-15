from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User


class FlexibleAuthBackend(ModelBackend):
    """
    Authenticate with username, email, or phone number.
    Falls back to Django's standard ModelBackend permission checks.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        identifier = username.strip()

        try:
            # Try to find user by username, email, or phone (case-insensitive for email)
            user = User.objects.get(
                Q(username__iexact=identifier) |
                Q(email__iexact=identifier) |
                Q(phone=identifier)
            )
        except User.DoesNotExist:
            # Run default password hasher to mitigate timing attacks
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # If multiple users share the same identifier (shouldn't happen), deny
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
