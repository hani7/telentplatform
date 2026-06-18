from django.contrib import admin
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display  = ("title", "sender", "recipient", "status", "created_at")
    list_filter   = ("status",)
    search_fields = ("title", "sender__username", "recipient__username")
    ordering      = ("-created_at",)
