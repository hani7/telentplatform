from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from accounts.models import User
from players.models import PlayerProfile
from coaches.models import CoachProfile
from .utils import split_by_visibility, get_viewer_context

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
@vary_on_cookie
@cache_page(60 * 5)
def players_list(request):
    if request.user.role not in [User.Role.CLUB, User.Role.AGENT]:
        return render(request, "search/players_list.html",
                      {"error": "Accès réservé aux Clubs/Agents."})

    qs = (
        PlayerProfile.objects
        .filter(is_active=True)
        .select_related("nationality")
        .only(*_PLAYER_LIST_FIELDS)
    )

    position   = (request.GET.get("position") or "").strip()
    country    = (request.GET.get("country") or "").strip()
    status     = (request.GET.get("status") or "").strip()
    has_filters = any([position, country, status])

    if not has_filters:
        qs = qs.order_by("-id")[:30]
    else:
        if position: qs = qs.filter(position__icontains=position)
        if status:   qs = qs.filter(status=status)
        if country:  qs = qs.filter(current_club_country__icontains=country)
        qs = qs.order_by("-id")[:50]

    viewer = get_viewer_context(request.user)
    results = split_by_visibility(
        qs,
        viewer_country=viewer["viewer_country"],
        viewer_division=viewer["viewer_division"],
        viewer_club=viewer["viewer_club"],
    )

    return render(request, "search/players_list.html", {
        "players": results,
        "has_filters": has_filters,
    })


@login_required
@vary_on_cookie
@cache_page(60 * 5)
def coaches_list(request):
    if request.user.role not in [User.Role.CLUB, User.Role.AGENT]:
        return render(request, "search/coaches_list.html",
                      {"error": "Accès réservé aux Clubs/Agents."})

    qs = (
        CoachProfile.objects
        .filter(is_active=True)
        .select_related("nationality")
        .only(*_COACH_LIST_FIELDS)
    )

    status     = (request.GET.get("status") or "").strip()
    country    = (request.GET.get("country") or "").strip()
    diploma_kw = (request.GET.get("diploma") or "").strip()
    has_filters = any([status, country, diploma_kw])

    if not has_filters:
        qs = qs.order_by("-id")[:30]
    else:
        if status:      qs = qs.filter(status=status)
        if country:     qs = qs.filter(current_club_country__icontains=country)
        if diploma_kw:  qs = qs.filter(diplomas_certificates__icontains=diploma_kw)
        qs = qs.order_by("-id")[:50]

    viewer = get_viewer_context(request.user)
    results = split_by_visibility(
        qs,
        viewer_country=viewer["viewer_country"],
        viewer_division=viewer["viewer_division"],
        viewer_club=viewer["viewer_club"],
    )

    return render(request, "search/coaches_list.html", {
        "coaches": results,
        "has_filters": has_filters,
    })
