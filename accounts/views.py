from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings

from .forms import LoginForm, BaseRegisterForm
from .models import User, OTPCode
from players.models import PlayerProfile
from coaches.models import CoachProfile
from agents.models import AgentProfile
from clubs.models import ClubProfile


class AppLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.role == User.Role.AGENT:
            return "/agents/dashboard/"
        if user.role == User.Role.CLUB:
            return "/clubs/dashboard/"
        if user.role == User.Role.PLAYER:
            return "/players/me/"
        if user.role == User.Role.COACH:
            return "/coaches/me/"
        return "/"


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


def _send_otp_email(user, otp):
    """Generate a new OTP for user and send it via email."""
    subject = "Votre code de vérification FOOTOP"
    message = (
        f"Bonjour {user.first_name or user.username},\n\n"
        f"Votre code de vérification FOOTOP est :\n\n"
        f"    {otp.code}\n\n"
        f"Ce code expire dans 10 minutes. Ne le partagez avec personne.\n\n"
        f"— L'équipe FOOTOP"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


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
            elif role == User.Role.AGENT:
                AgentProfile.objects.create(
                    user=user,
                    first_name=user.first_name or "",
                    last_name=user.last_name or "",
                )
            elif role == User.Role.CLUB:
                ClubProfile.objects.create(
                    user=user,
                    club_name=user.first_name or "",
                )

            # Generate OTP and send email
            otp = OTPCode.generate_for(user)
            _send_otp_email(user, otp)

            # Store user id in session for the verify step
            request.session["otp_user_id"] = user.pk
            request.session["otp_role"] = role

            return redirect("accounts:verify_otp")
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


@require_http_methods(["GET", "POST"])
def verify_otp(request):
    user_id = request.session.get("otp_user_id")
    if not user_id:
        return redirect("accounts:register_role")

    user = get_object_or_404(User, pk=user_id)
    error = None

    if request.method == "POST":
        entered_code = request.POST.get("otp_code", "").strip()
        otp = (
            OTPCode.objects.filter(user=user, is_used=False)
            .order_by("-created_at")
            .first()
        )

        if otp is None:
            error = "Aucun code actif. Veuillez renvoyer un nouveau code."
        elif otp.is_expired():
            otp.is_used = True
            otp.save()
            error = "Ce code a expiré. Veuillez en demander un nouveau."
        elif otp.code != entered_code:
            error = "Code incorrect. Veuillez réessayer."
        else:
            # Mark OTP used + verify user
            otp.is_used = True
            otp.save()
            user.is_verified = True
            user.save(update_fields=["is_verified"])

            # Clean up session and log the user in
            role = request.session.pop("otp_role", None)
            del request.session["otp_user_id"]

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "Compte vérifié ✅ Bienvenue sur FOOTOP !")

            if role == User.Role.PLAYER:
                return redirect("players:profile_edit")
            if role == User.Role.COACH:
                return redirect("coaches:profile_edit")
            if role == User.Role.AGENT:
                return redirect("agents:profile_edit")
            if role == User.Role.CLUB:
                return redirect("clubs:profile_edit")
            return redirect("home")

    return render(request, "accounts/verify_otp.html", {
        "email": user.email,
        "error": error,
    })


@require_POST
def resend_otp(request):
    user_id = request.session.get("otp_user_id")
    if not user_id:
        return redirect("accounts:register_role")

    user = get_object_or_404(User, pk=user_id)
    otp = OTPCode.generate_for(user)
    _send_otp_email(user, otp)
    messages.info(request, "Un nouveau code a été envoyé à votre adresse email.")
    return redirect("accounts:verify_otp")


def logout_view(request):
    logout(request)
    return redirect("home")
