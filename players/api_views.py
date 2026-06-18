from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from .models import PlayerProfile
from .serializers import PlayerProfileSerializer, PlayerListSerializer


class APIPlayerProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/players/profile/ — own profile"""
    serializer_class = PlayerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = PlayerProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'first_name': self.request.user.first_name or '',
                'last_name': self.request.user.last_name or '',
            }
        )
        return profile


class APIPlayerPublicView(generics.RetrieveAPIView):
    """GET /api/players/public/<pk>/"""
    serializer_class = PlayerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PlayerProfile.objects.filter(is_active=True)


class APIPlayersListView(generics.ListAPIView):
    """GET /api/players/list/ — paginated, filterable"""
    serializer_class = PlayerListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'position', 'current_club_name']
    ordering_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = PlayerProfile.objects.filter(is_active=True)
        position = self.request.query_params.get('position')
        status_filter = self.request.query_params.get('status')
        nationality = self.request.query_params.get('nationality')
        if position:
            qs = qs.filter(position__icontains=position)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if nationality:
            qs = qs.filter(nationality__name__icontains=nationality)
        return qs
