from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [
    path("me/", views.club_profile_edit, name="profile_edit"),
    path("dashboard/", views.club_dashboard, name="dashboard"),
    path("send-offer/", views.club_send_offer, name="send_offer"),
]
