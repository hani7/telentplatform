from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from accounts.models import User
from players.models import PlayerProfile
from coaches.models import CoachProfile
from offers.models import Offer
from search.utils import split_by_visibility, get_viewer_context
from .models import ClubProfile
from .forms import ClubProfileForm

# Minimum columns for list rendering
_PLAYER_LIST_FIELDS = (
    "id", "first_name", "last_name", "position", "status", "foot",
    "height_cm", "desired_salary", "availability",
    "current_club_name", "current_club_country",
    "nationality_id",
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
def club_profile_edit(request):
    """Club profile completion / edit page."""
    profile, _ = ClubProfile.objects.get_or_create(
        user=request.user,
        defaults={"club_name": request.user.first_name or ""},
    )

    if request.method == "POST":
        form = ClubProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil club mis à jour ✅")
            return redirect("clubs:profile_edit")
    else:
        form = ClubProfileForm(instance=profile)

    return render(request, "clubs/profile_edit.html", {"form": form, "profile": profile})


@login_required
@vary_on_cookie
@cache_page(60 * 5)                # ✅ cache dashboard HTML for 5 minutes
def club_dashboard(request):
    """
    Club dashboard: browse players + coaches with filters.
    Same optimisations as agent_dashboard (only, select_related, split_by_visibility).
    """
    if request.user.role != User.Role.CLUB:
        messages.error(request, "Accès réservé aux Clubs.")
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
            .only(*_PLAYER_LIST_FIELDS)
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

        qs = qs.order_by("-id")[:50]
        players = split_by_visibility(
            qs,
            viewer_country=viewer["viewer_country"],
            viewer_division=viewer["viewer_division"],
            viewer_club=viewer["viewer_club"],
        )

    # ── Coaches ────────────────────────────────────────────────────────────────
    if role_filter in ("ALL", "COACH"):
        qs = (
            CoachProfile.objects
            .filter(is_active=True)
            .select_related("nationality")
            .only(*_COACH_LIST_FIELDS)
        )

        if role_filter == "COACH":
            status     = (request.GET.get("status") or "").strip()
            country    = (request.GET.get("country") or "").strip()
            diploma_kw = (request.GET.get("diploma") or "").strip()

            if status:      qs = qs.filter(status=status)
            if country:     qs = qs.filter(current_club_country__icontains=country)
            if diploma_kw:  qs = qs.filter(diplomas_certificates__icontains=diploma_kw)

        qs = qs.order_by("-id")[:50]
        coaches = split_by_visibility(
            qs,
            viewer_country=viewer["viewer_country"],
            viewer_division=viewer["viewer_division"],
            viewer_club=viewer["viewer_club"],
        )

    return render(request, "clubs/dashboard.html", {
        "role_filter": role_filter,
        "players": players,
        "coaches": coaches,
    })


@login_required
def club_send_offer(request):
    """Quick offer send from club dashboard (POST only)."""
    if request.user.role != User.Role.CLUB:
        messages.error(request, "Accès réservé aux Clubs.")
        return redirect("home")

    if request.method == "POST":
        recipient_id = request.POST.get("recipient_id")
        title        = request.POST.get("title", "").strip()
        message_text = request.POST.get("message", "").strip()

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

    return redirect("clubs:dashboard")
