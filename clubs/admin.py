from django.contrib import admin
from .models import ClubProfile


@admin.register(ClubProfile)
class ClubProfileAdmin(admin.ModelAdmin):
    list_display = ("club_name", "function", "user", "is_active")
    search_fields = ("club_name",)
