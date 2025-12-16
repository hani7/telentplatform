from django.urls import path
from . import views

app_name = "players"

urlpatterns = [
    path("me/", views.player_profile_edit, name="profile_edit"),
    path("me/activate/", views.player_activate_ad, name="activate_ad"),
    path("me/deactivate/", views.player_deactivate_ad, name="deactivate_ad"),
    path("p/<int:pk>/", views.player_public_profile, name="public_profile"),
]
