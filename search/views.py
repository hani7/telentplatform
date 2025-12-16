from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import User
from players.models import PlayerProfile
from coaches.models import CoachProfile
from .utils import is_allowed_by_visibility


def _viewer_context(user):
    # MVP: on n'a pas encore ClubProfile/AgentProfile => on utilise juste username comme "club"
    return {
        "viewer_club": user.username if user.is_authenticated else None,
        "viewer_country": None,
        "viewer_division": None,
    }


@login_required
def players_list(request):
    if request.user.role not in [User.Role.CLUB, User.Role.AGENT]:
        return render(request, "search/players_list.html", {"error": "Accès réservé aux Clubs/Agents."})

    qs = PlayerProfile.objects.filter(is_active=True).select_related("nationality")

    # filtres GET (inchangé)
    position = (request.GET.get("position") or "").strip()
    country = (request.GET.get("country") or "").strip()
    status = (request.GET.get("status") or "").strip()

    # ✅ détecter si on est en mode filtre
    has_filters = any([position, country, status])

    # ✅ Si pas de filtres : afficher une liste par défaut (ex: derniers profils)
    if not has_filters:
        qs = qs.order_by("-id")[:30]   # tu peux changer 30

    # ✅ Si filtres présents : appliquer filtres
    else:
        if position:
            qs = qs.filter(position__icontains=position)
        if status:
            qs = qs.filter(status=status)
        if country:
            qs = qs.filter(current_club_country__icontains=country)

    viewer = _viewer_context(request.user)

    # appliquer visibilité en python (MVP) - inchangé
    results = []
    for p in qs:
        if is_allowed_by_visibility(
            p.visibility_mode, p.visibility_filters, p.visibility_exceptions,
            viewer_country=viewer["viewer_country"],
            viewer_division=viewer["viewer_division"],
            viewer_club=viewer["viewer_club"]
        ):
            results.append(p)

    return render(
        request,
        "search/players_list.html",
        {
            "players": results,
            "has_filters": has_filters,  # ✅ pour template
        }
    )


@login_required
def coaches_list(request):
    if request.user.role not in [User.Role.CLUB, User.Role.AGENT]:
        return render(request, "search/coaches_list.html", {"error": "Accès réservé aux Clubs/Agents."})

    qs = CoachProfile.objects.filter(is_active=True).select_related("nationality")

    status = (request.GET.get("status") or "").strip()
    country = (request.GET.get("country") or "").strip()
    diploma_kw = (request.GET.get("diploma") or "").strip()

    # ✅ détecter si on est en mode filtre
    has_filters = any([status, country, diploma_kw])

    # ✅ Si pas de filtres : afficher une liste par défaut
    if not has_filters:
        qs = qs.order_by("-id")[:30]  # tu peux changer 30
    else:
        # filtres (inchangé)
        if status:
            qs = qs.filter(status=status)
        if country:
            qs = qs.filter(current_club_country__icontains=country)
        if diploma_kw:
            qs = qs.filter(diplomas_certificates__icontains=diploma_kw)

    viewer = _viewer_context(request.user)

    results = []
    for c in qs:
        if is_allowed_by_visibility(
            c.visibility_mode, c.visibility_filters, c.visibility_exceptions,
            viewer_country=viewer["viewer_country"],
            viewer_division=viewer["viewer_division"],
            viewer_club=viewer["viewer_club"]
        ):
            results.append(c)

    return render(
        request,
        "search/coaches_list.html",
        {
            "coaches": results,
            "has_filters": has_filters,  # ✅ pour template
        }
    )
