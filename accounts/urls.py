from django.urls import path
from .views import AppLoginView, register_role, register_player, register_coach, register_agent, register_club, logout_view

app_name = "accounts"

urlpatterns = [
    path("login/", AppLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_role, name="register_role"),
    path("register/player/", register_player, name="register_player"),
    path("register/coach/", register_coach, name="register_coach"),
    path("register/agent/", register_agent, name="register_agent"),
    path("register/club/", register_club, name="register_club"),
]
