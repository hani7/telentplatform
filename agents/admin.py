from django.contrib import admin
from .models import AgentProfile


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "license_number", "specialization", "is_active"]
    list_filter = ["specialization", "is_active"]
    search_fields = ["first_name", "last_name", "license_number", "agency_name"]
