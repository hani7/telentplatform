from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from accounts.models import User
from players.models import PlayerProfile, Nationality
from coaches.models import CoachProfile
from offers.models import Offer
from search.utils import split_by_visibility, get_viewer_context
from .models import AgentProfile
from .forms import AgentProfileForm

# Fields needed for display in the dashboard list — fetch only these
_PLAYER_LIST_FIELDS = (
    "id", "first_name", "last_name", "position", "status", "foot",
    "height_cm", "desired_salary", "availability",
    "current_club_name", "current_club_country",
    "nationality_id",                    # FK id — avoids extra join when nationality already selected
    "visibility_mode", "visibility_filters", "visibility_exceptions",
    "user_id",
)
_COACH_LIST_FIELDS = (
    "id", "first_name", "last_name", "status",
    "current_club_name", "current_club_country",
    "diplomas_certificates",
    "nationality_id",
    "visibility_mode", "visibility_filters", "visibility_exceptions",
    "user_id",
)


@login_required
def agent_profile_edit(request):
    """Agent profile completion / edit page."""
    profile, _ = AgentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "first_name": request.user.first_name or "",
            "last_name": request.user.last_name or "",
        },
    )

    if request.method == "POST":
        form = AgentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil agent mis à jour ✅")
            return redirect("agents:profile_edit")
    else:
        form = AgentProfileForm(instance=profile)

    return render(request, "agents/profile_edit.html", {
        "form": form,
        "profile": profile,
        "nationalities": Nationality.objects.all().order_by("name"),
    })


@login_required
@vary_on_cookie                     # ✅ cache per-user (different agents see same data)
@cache_page(60 * 5)                 # ✅ cache dashboard HTML for 5 minutes
def agent_dashboard(request):
    """
    Agent dashboard: combined list of players and coaches.
    Optimisations:
      - only() fetches the minimum columns (no heavy TextFields, no dates)
      - select_related('nationality') avoids N+1 on nationality name
      - split_by_visibility() does DB-level fast path for ALL mode
    """
    if request.user.role != User.Role.AGENT:
        messages.error(request, "Accès réservé aux Agents.")
        return redirect("home")

    role_filter = request.GET.get("role", "ALL")
    viewer = get_viewer_context(request.user)

    players = []
    coaches = []

    # ── Players ────────────────────────────────────────────────────────────────
    if role_filter in ("ALL", "PLAYER"):
        qs = (
            PlayerProfile.objects
            .filter(is_active=True)
            .select_related("nationality")
            .only(*_PLAYER_LIST_FIELDS)          # ✅ fetch minimum columns
        )

        if role_filter == "PLAYER":
            position   = (request.GET.get("position") or "").strip()
            country    = (request.GET.get("country") or "").strip()
            status     = (request.GET.get("status") or "").strip()
            foot       = (request.GET.get("foot") or "").strip()
            height_min = request.GET.get("height_min")
            height_max = request.GET.get("height_max")
            salary_min = request.GET.get("salary_min")
            salary_max = request.GET.get("salary_max")

            if position:    qs = qs.filter(position__icontains=position)
            if country:     qs = qs.filter(current_club_country__icontains=country)
            if status:      qs = qs.filter(status=status)
            if foot:        qs = qs.filter(foot=foot)
            if height_min:  qs = qs.filter(height_cm__gte=int(height_min))
            if height_max:  qs = qs.filter(height_cm__lte=int(height_max))
            if salary_min:  qs = qs.filter(desired_salary__gte=int(salary_min))
            if salary_max:  qs = qs.filter(desired_salary__lte=int(salary_max))

        qs = qs.order_by("-id")  # unsliced — split_by_visibility slices internally

        # ✅ split_by_visibility: ALL-mode profiles via DB filter, others in Python
        players = split_by_visibility(
            qs,
            viewer_country=viewer["viewer_country"],
            viewer_division=viewer["viewer_division"],
            viewer_club=viewer["viewer_club"],
            limit=50,
        )

    # ── Coaches ────────────────────────────────────────────────────────────────
    if role_filter in ("ALL", "COACH"):
        qs = (
            CoachProfile.objects
            .filter(is_active=True)
            .select_related("nationality")
            .only(*_COACH_LIST_FIELDS)           # ✅ fetch minimum columns
        )

        if role_filter == "COACH":
            status     = (request.GET.get("status") or "").strip()
            country    = (request.GET.get("country") or "").strip()
            diploma_kw = (request.GET.get("diploma") or "").strip()

            if status:      qs = qs.filter(status=status)
            if country:     qs = qs.filter(current_club_country__icontains=country)
            if diploma_kw:  qs = qs.filter(diplomas_certificates__icontains=diploma_kw)

        qs = qs.order_by("-id")  # unsliced — split_by_visibility slices internally

        coaches = split_by_visibility(
            qs,
            viewer_country=viewer["viewer_country"],
            viewer_division=viewer["viewer_division"],
            viewer_club=viewer["viewer_club"],
            limit=50,
        )

    return render(request, "agents/dashboard.html", {
        "role_filter": role_filter,
        "players": players,
        "coaches": coaches,
    })


@login_required
def agent_send_offer(request):
    """Quick offer send from dashboard (POST only)."""
    if request.user.role != User.Role.AGENT:
        messages.error(request, "Accès réservé aux Agents.")
        return redirect("home")

    if request.method == "POST":
        recipient_id  = request.POST.get("recipient_id")
        title         = request.POST.get("title", "").strip()
        message_text  = request.POST.get("message", "").strip()

        if not recipient_id or not title or not message_text:
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            recipient = get_object_or_404(
                User.objects.only("id", "role", "first_name", "last_name", "username"),
                pk=recipient_id
            )
            if recipient.role not in (User.Role.PLAYER, User.Role.COACH):
                messages.error(request, "Destinataire invalide.")
            else:
                Offer.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    title=title,
                    message=message_text,
                )
                messages.success(
                    request,
                    f"Offre envoyée à {recipient.get_full_name() or recipient.username} ✅",
                )

    return redirect("agents:dashboard")
