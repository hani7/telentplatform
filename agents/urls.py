from django.urls import path
from . import views

app_name = "agents"

urlpatterns = [
    path("me/", views.agent_profile_edit, name="profile_edit"),
    path("dashboard/", views.agent_dashboard, name="dashboard"),
    path("send-offer/", views.agent_send_offer, name="send_offer"),
]
