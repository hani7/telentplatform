from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    path("players/", views.players_list, name="players_list"),
    path("coaches/", views.coaches_list, name="coaches_list"),
]
