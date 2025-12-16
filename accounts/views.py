from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.views import LoginView

from .forms import LoginForm, BaseRegisterForm
from .models import User
from players.models import PlayerProfile
from coaches.models import CoachProfile

class AppLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

@require_http_methods(["GET", "POST"])
def register_role(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role not in dict(User.Role.choices):
            messages.error(request, "Choisis un rôle valide.")
            return redirect("accounts:register_role")

        if role == User.Role.PLAYER:
            return redirect("accounts:register_player")
        if role == User.Role.COACH:
            return redirect("accounts:register_coach")
        if role == User.Role.AGENT:
            return redirect("accounts:register_agent")
        if role == User.Role.CLUB:
            return redirect("accounts:register_club")

    return render(request, "accounts/register_role.html")

def _register_generic(request, role, template_name):
    if request.method == "POST":
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(role=role)

            if role == User.Role.PLAYER:
                PlayerProfile.objects.create(
                    user=user,
                    first_name=user.first_name or "",
                    last_name=user.last_name or "",
                )
            elif role == User.Role.COACH:
                CoachProfile.objects.create(
                    user=user,
                    first_name=user.first_name or "",
                    last_name=user.last_name or "",
                )

            login(request, user)
            messages.success(request, "Compte créé ✅")
            if role == User.Role.PLAYER:
                return redirect("players:profile_edit")
            if role == User.Role.COACH:
                return redirect("coaches:profile_edit")
            return redirect("home")
    else:
        form = BaseRegisterForm()

    return render(request, template_name, {"form": form})

def register_player(request):
    return _register_generic(request, User.Role.PLAYER, "accounts/register_player.html")

def register_coach(request):
    return _register_generic(request, User.Role.COACH, "accounts/register_coach.html")

def register_agent(request):
    return _register_generic(request, User.Role.AGENT, "accounts/register_agent.html")

def register_club(request):
    return _register_generic(request, User.Role.CLUB, "accounts/register_club.html")

def logout_view(request):
    logout(request)
    return redirect("home")
