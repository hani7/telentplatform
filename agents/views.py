from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import User
from players.models import PlayerProfile, Nationality
from coaches.models import CoachProfile
from offers.models import Offer
from search.utils import is_allowed_by_visibility
from .models import AgentProfile
from .forms import AgentProfileForm, AgentFileFormSet


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
        form = AgentProfileForm(request.POST, request.FILES, instance=profile)
        files_fs = AgentFileFormSet(request.POST, request.FILES, instance=profile, prefix="files")
        
        if form.is_valid() and files_fs.is_valid():
            form.save()
            files_fs.save()
            messages.success(request, "Profil agent mis à jour ✅")
            return redirect("agents:profile_edit")
    else:
        form = AgentProfileForm(instance=profile)
        files_fs = AgentFileFormSet(instance=profile, prefix="files")

    return render(request, "agents/profile_edit.html", {
        "form": form,
        "files_fs": files_fs,
        "profile": profile,
        "nationalities": Nationality.objects.all().order_by("name"),
    })


def _viewer_context(user):
    return {
        "viewer_club": user.username if user.is_authenticated else None,
        "viewer_country": None,
        "viewer_division": None,
    }


@login_required
def agent_dashboard(request):
    """
    Agent dashboard: combined list of players and coaches with role-based filters
    and ability to send offers.
    """
    if request.user.role != User.Role.AGENT:
        messages.error(request, "Accès réservé aux Agents.")
        return redirect("home")

    role_filter = request.GET.get("role", "ALL")  # default: show all
    viewer = _viewer_context(request.user)

    players = []
    coaches = []

    # ── Load players (when ALL or PLAYER) ──
    if role_filter in ("ALL", "PLAYER"):
        qs = PlayerProfile.objects.filter(is_active=True).select_related("nationality")

        if role_filter == "PLAYER":
            # Player-specific filters only when role is explicitly PLAYER
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

    # ── Load coaches (when ALL or COACH) ──
    if role_filter in ("ALL", "COACH"):
        qs = CoachProfile.objects.filter(is_active=True).select_related("nationality")

        if role_filter == "COACH":
            # Coach-specific filters only when role is explicitly COACH
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

    return redirect("agents:dashboard")
