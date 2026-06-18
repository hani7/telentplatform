from rest_framework import generics, permissions
from .models import CoachProfile
from .serializers import CoachProfileSerializer


class APICoachProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/coaches/profile/ — own profile"""
    serializer_class = CoachProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = CoachProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'first_name': self.request.user.first_name or '',
                'last_name': self.request.user.last_name or '',
            }
        )
        return profile
