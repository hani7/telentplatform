from django.urls import path
from . import views

app_name = "coaches"

urlpatterns = [
    path("me/", views.coach_profile_edit, name="profile_edit"),
    path("me/activate/", views.coach_activate_ad, name="activate_ad"),
    path("me/deactivate/", views.coach_deactivate_ad, name="deactivate_ad"),
    path("p/<int:pk>/", views.coach_public_profile, name="public_profile"),
]
