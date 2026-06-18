from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import User
from players.models import PlayerProfile
from coaches.models import CoachProfile
from offers.models import Offer
from search.utils import is_allowed_by_visibility
from .models import ClubProfile
from .forms import ClubProfileForm


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


def _viewer_context(user):
    return {
        "viewer_club": user.username if user.is_authenticated else None,
        "viewer_country": None,
        "viewer_division": None,
    }


@login_required
def club_dashboard(request):
    """Club dashboard: combined list of players and coaches with role-based filters."""
    if request.user.role != User.Role.CLUB:
        messages.error(request, "Accès réservé aux Clubs.")
        return redirect("home")

    role_filter = request.GET.get("role", "ALL")
    viewer = _viewer_context(request.user)

    players = []
    coaches = []

    if role_filter in ("ALL", "PLAYER"):
        qs = PlayerProfile.objects.filter(is_active=True).select_related("nationality")

        if role_filter == "PLAYER":
            position = (request.GET.get("position") or "").strip()
            country = (request.GET.get("country") or "").strip()
            status = (request.GET.get("status") or "").strip()
            foot = (request.GET.get("foot") or "").strip()
            height_min = request.GET.get("height_min")
            height_max = request.GET.get("height_max")
            salary_min = request.GET.get("salary_min")
            salary_max = request.GET.get("salary_max")

            if position:
                qs = qs.filter(position__icontains=position)
            if country:
                qs = qs.filter(current_club_country__icontains=country)
            if status:
                qs = qs.filter(status=status)
            if foot:
                qs = qs.filter(foot=foot)
            if height_min:
                qs = qs.filter(height_cm__gte=int(height_min))
            if height_max:
                qs = qs.filter(height_cm__lte=int(height_max))
            if salary_min:
                qs = qs.filter(salary_min__gte=int(salary_min))
            if salary_max:
                qs = qs.filter(salary_max__lte=int(salary_max))

        qs = qs.order_by("-id")[:50]

        for p in qs:
            if is_allowed_by_visibility(
                p.visibility_mode, p.visibility_filters, p.visibility_exceptions,
                viewer_country=viewer["viewer_country"],
                viewer_division=viewer["viewer_division"],
                viewer_club=viewer["viewer_club"],
            ):
                players.append(p)

    if role_filter in ("ALL", "COACH"):
        qs = CoachProfile.objects.filter(is_active=True).select_related("nationality")

        if role_filter == "COACH":
            status = (request.GET.get("status") or "").strip()
            country = (request.GET.get("country") or "").strip()
            diploma_kw = (request.GET.get("diploma") or "").strip()

            if status:
                qs = qs.filter(status=status)
            if country:
                qs = qs.filter(current_club_country__icontains=country)
            if diploma_kw:
                qs = qs.filter(diplomas_certificates__icontains=diploma_kw)

        qs = qs.order_by("-id")[:50]

        for c in qs:
            if is_allowed_by_visibility(
                c.visibility_mode, c.visibility_filters, c.visibility_exceptions,
                viewer_country=viewer["viewer_country"],
                viewer_division=viewer["viewer_division"],
                viewer_club=viewer["viewer_club"],
            ):
                coaches.append(c)

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
        title = request.POST.get("title", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not recipient_id or not title or not message_text:
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            recipient = get_object_or_404(User, pk=recipient_id)
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
