from django import template
import re

register = template.Library()

# A mapping of common French country names to ISO 3166-1 alpha-2 codes (lowercase for flagcdn)
COUNTRY_TO_ISO = {
    'algérie': 'dz',
    'france': 'fr',
    'maroc': 'ma',
    'tunisie': 'tn',
    'birmanie': 'mm',
    'sénégal': 'sn',
    'côte d\'ivoire': 'ci',
    'cameroun': 'cm',
    'mali': 'ml',
    'belgique': 'be',
    'suisse': 'ch',
    'canada': 'ca',
    'espagne': 'es',
    'italie': 'it',
    'angleterre': 'gb-eng',
    'allemagne': 'de',
    'brésil': 'br',
    'argentine': 'ar',
    'portugal': 'pt',
    'états-unis': 'us',
    'arabie saoudite': 'sa',
    'qatar': 'qa',
    'égypte': 'eg',
    'nigéria': 'ng',
    'ghana': 'gh',
    'afrique du sud': 'za',
    'congo (rdc)': 'cd',
    'gabon': 'ga',
    'guinée': 'gn',
    'madagascar': 'mg',
    'maurice': 'mu',
    'pays-bas': 'nl',
    'turquie': 'tr',
    'suède': 'se',
    'norvège': 'no',
    'danemark': 'dk',
    'japon': 'jp',
    'corée du sud': 'kr',
    'australie': 'au',
    'chine': 'cn',
    'inde': 'in',
    'russie': 'ru',
    'pologne': 'pl',
    'croatie': 'hr',
    'serbie': 'rs',
    'uruguay': 'uy',
    'colombie': 'co',
    'chili': 'cl',
    'mexique': 'mx',
    'iran': 'ir',
    'emirats arabes unis': 'ae',
}

@register.filter
def flag_url(country_name):
    """
    Returns the URL to the flag image for a given country name using flagcdn.
    Returns None if the country is not recognized or is empty.
    """
    if not country_name:
        return None
    
    # Normalize the country name
    normalized = str(country_name).lower().strip()
    
    # Check manual mapping first
    iso_code = COUNTRY_TO_ISO.get(normalized)
    
    if iso_code:
        return f"https://flagcdn.com/w40/{iso_code}.png"
    
    # If not found, we could attempt a heuristic, but returning None 
    # allows the template to fallback to a generic icon.
    return None
