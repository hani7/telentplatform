"""
search/utils.py
Shared visibility engine and query helpers.
"""
from django.db.models import QuerySet


# ─── Internal helper ─────────────────────────────────────────────────────────

def _get_list(d, key):
    if not isinstance(d, dict):
        return []
    v = d.get(key, [])
    return v if isinstance(v, list) else []


# ─── Visibility check (Python-level, after queryset is fetched) ───────────────

def is_allowed_by_visibility(mode, filters_dict, exceptions_dict,
                              viewer_country=None, viewer_division=None, viewer_club=None):
    """
    Returns True if the viewer is allowed to see a profile with the given
    visibility settings.
    """
    if mode == "ALL":
        return True

    if mode == "ALL_EXCEPT":
        exc_countries = _get_list(exceptions_dict, "countries")
        exc_divisions = _get_list(exceptions_dict, "divisions")
        exc_clubs     = _get_list(exceptions_dict, "clubs")

        if viewer_country  and viewer_country  in exc_countries:  return False
        if viewer_division and viewer_division in exc_divisions:   return False
        if viewer_club     and viewer_club     in exc_clubs:       return False
        return True

    if mode == "SOME":
        allow_countries = _get_list(filters_dict, "countries")
        allow_divisions = _get_list(filters_dict, "divisions")
        allow_clubs     = _get_list(filters_dict, "clubs")

        if not (allow_countries or allow_divisions or allow_clubs):
            return False

        if viewer_club     and allow_clubs     and viewer_club     in allow_clubs:     return True
        if viewer_country  and allow_countries and viewer_country  in allow_countries: return True
        if viewer_division and allow_divisions and viewer_division in allow_divisions: return True

        return False

    return True  # unknown mode → allow


# ─── Fast DB-level pre-split ─────────────────────────────────────────────────

def split_by_visibility(qs, viewer_country=None, viewer_division=None,
                        viewer_club=None, limit=50):
    """
    Efficiently filter a queryset down to visible profiles.

    IMPORTANT: pass an ORDERED but UN-SLICED queryset. The slice is applied
    internally. Passing a sliced queryset would cause:
        TypeError: Cannot filter a query once a slice has been taken.

    Strategy:
      1. Profiles with visibility_mode='ALL' → always visible, fetched via
         an indexed DB filter (fast path, no Python evaluation needed).
      2. Profiles with ALL_EXCEPT / SOME → small subset, checked in Python.

    Returns a list of at most `limit` visible model instances.
    """
    # Fast path: ALL-mode profiles are always visible.
    # The DB index on visibility_mode makes this very fast.
    always_visible = list(qs.filter(visibility_mode="ALL")[:limit])

    if len(always_visible) >= limit:
        return always_visible

    # Need more results — check conditional-mode profiles in Python.
    remaining = limit - len(always_visible)
    # Fetch 3× remaining to account for profiles that fail the Python check.
    pool = list(qs.exclude(visibility_mode="ALL")[:remaining * 3])

    conditional_visible = [
        p for p in pool
        if is_allowed_by_visibility(
            p.visibility_mode, p.visibility_filters, p.visibility_exceptions,
            viewer_country=viewer_country,
            viewer_division=viewer_division,
            viewer_club=viewer_club,
        )
    ][:remaining]

    return always_visible + conditional_visible


# ─── Viewer context ───────────────────────────────────────────────────────────

def get_viewer_context(user):
    """
    Build viewer metadata for visibility checks.
    Shared by agents/views.py, clubs/views.py, and search/views.py.
    """
    return {
        "viewer_club":     user.username if user.is_authenticated else None,
        "viewer_country":  None,
        "viewer_division": None,
    }
