import json
import urllib.request
import urllib.parse
from django.http import JsonResponse
from django.conf import settings

def search_clubs_api(request):
    """
    Proxy view for searching football clubs via TheSportsDB (Free Public API).
    Provides a massive database of clubs and information.
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})

    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={urllib.parse.quote(query)}"
    req = urllib.request.Request(url)
    # TheSportsDB recommends a user agent
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                teams = data.get('teams')
                
                if not teams:
                    return JsonResponse({'results': []})
                
                COUNTRY_MAP = {
                    "England": "Royaume-Uni",
                    "Spain": "Espagne",
                    "Italy": "Italie",
                    "Germany": "Allemagne",
                    "Algeria": "Algérie",
                    "Netherlands": "Pays-Bas",
                    "Belgium": "Belgique",
                    "Brazil": "Brésil",
                    "Argentina": "Argentine",
                    "Morocco": "Maroc",
                    "Tunisia": "Tunisie",
                    "Egypt": "Égypte",
                    "Turkey": "Turquie",
                    "Russia": "Russie",
                    "Switzerland": "Suisse",
                    "Scotland": "Royaume-Uni",
                    "Wales": "Royaume-Uni"
                }
                
                formatted_results = []
                for team in teams:
                    # Filter to only include Soccer (Football) teams to avoid NFL/NBA teams if names overlap
                    if team.get('strSport', '').lower() != 'soccer':
                        continue
                        
                    en_country = team.get('strCountry', '')
                    fr_country = COUNTRY_MAP.get(en_country, en_country)
                        
                    formatted_results.append({
                        "name": team.get('strTeam'),
                        "logo": team.get('strBadge'),
                        "country": fr_country,
                        "division": team.get('strLeague', '')
                    })
                return JsonResponse({'results': formatted_results})
            else:
                return JsonResponse({'error': 'API Error'}, status=response.status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
