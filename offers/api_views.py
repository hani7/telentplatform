from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Offer
from .serializers import OfferSerializer
from accounts.models import User


class APIMyOffersView(generics.ListAPIView):
    """GET /api/offers/my/ — offers received by the current user (PLAYER/COACH)"""
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Offer.objects.filter(recipient=self.request.user)


class APIMySuggestionsView(generics.ListAPIView):
    """GET /api/offers/suggestions/ — offers sent by current user (AGENT/CLUB)"""
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Offer.objects.filter(sender=self.request.user)


class APISendOfferView(generics.CreateAPIView):
    """POST /api/offers/send/ — AGENT/CLUB sends offer to a player/coach"""
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class APIOfferRespondView(APIView):
    """POST /api/offers/<pk>/respond/ — {action: 'accept'|'decline'}"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk, recipient=request.user)
        action = request.data.get('action', '')
        if action == 'accept':
            offer.status = Offer.Status.ACCEPTED
        elif action == 'decline':
            offer.status = Offer.Status.DECLINED
        else:
            return Response({'detail': 'Action invalide. Utilisez "accept" ou "decline".'}, status=status.HTTP_400_BAD_REQUEST)
        offer.save(update_fields=['status', 'updated_at'])
        return Response(OfferSerializer(offer).data)
