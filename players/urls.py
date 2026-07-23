from django.urls import path
from . import views
from . import views_api

app_name = "players"

urlpatterns = [
    path("me/", views.player_profile_edit, name="profile_edit"),
    path("me/complete/", views.profile_complete, name="profile_complete"),
    path("me/success/", views.profile_success, name="profile_success"),
    path("me/activate/", views.player_activate_ad, name="activate_ad"),
    path("me/deactivate/", views.player_deactivate_ad, name="deactivate_ad"),
    path("consent/verify/<uuid:token>/", views.verify_consent, name="verify_consent"),
    path("p/<int:pk>/", views.player_public_profile, name="public_profile"),
    path("api/clubs/search/", views_api.search_clubs_api, name="api_clubs_search"),
    path("api/clubs/division/", views_api.get_team_division_api, name="api_clubs_division"),
]
