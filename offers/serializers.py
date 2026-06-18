from rest_framework import serializers
from .models import Offer
from accounts.serializers import UserSerializer


class OfferSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'message', 'status', 'status_display',
            'sender', 'sender_name', 'sender_role',
            'recipient', 'recipient_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'sender', 'status', 'created_at', 'updated_at']
