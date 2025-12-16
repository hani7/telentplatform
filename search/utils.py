def _get_list(d, key):
    if not isinstance(d, dict):
        return []
    v = d.get(key, [])
    return v if isinstance(v, list) else []

def is_allowed_by_visibility(mode, filters_dict, exceptions_dict, viewer_country=None, viewer_division=None, viewer_club=None):
    # viewer_* : infos du club/agent (si tu veux). MVP: club name suffit.
    if mode == "ALL":
        return True

    if mode == "ALL_EXCEPT":
        exc_countries = _get_list(exceptions_dict, "countries")
        exc_divisions = _get_list(exceptions_dict, "divisions")
        exc_clubs = _get_list(exceptions_dict, "clubs")

        if viewer_country and viewer_country in exc_countries:
            return False
        if viewer_division and viewer_division in exc_divisions:
            return False
        if viewer_club and viewer_club in exc_clubs:
            return False
        return True

    if mode == "SOME":
        allow_countries = _get_list(filters_dict, "countries")
        allow_divisions = _get_list(filters_dict, "divisions")
        allow_clubs = _get_list(filters_dict, "clubs")

        # si aucune règle => rien n'est visible
        if not (allow_countries or allow_divisions or allow_clubs):
            return False

        if viewer_club and allow_clubs and viewer_club in allow_clubs:
            return True
        if viewer_country and allow_countries and viewer_country in allow_countries:
            return True
        if viewer_division and allow_divisions and viewer_division in allow_divisions:
            return True

        return False

    return True
