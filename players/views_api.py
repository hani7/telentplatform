import json
import urllib.request
import urllib.parse
from django.http import JsonResponse
from django.conf import settings

def search_clubs_api(request):
    """
    Proxy view for searching football clubs via API-Sports (API-Football).
    Uses the API key provided in settings.
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})

    query_lower = query.lower()
    ALIASES = {
        "psg": "paris saint germain",
        "fcb": "barcelona",
        "mca": "mc alger",
        "jsk": "js kabylie",
        "usma": "usm alger",
        "crb": "cr belouizdad",
        "mco": "mc oran",
        "csc": "cs constantine",
        "ess": "es setif",
        "om": "marseille",
        "ol": "lyon",
        "bvb": "dortmund",
        "rma": "real madrid",
        "lfc": "liverpool",
        "mci": "manchester city",
        "man u": "manchester united",
        "atm": "atletico madrid",
        "acm": "ac milan",
        "rca": "raja",
        "wac": "wydad"
    }

    OFFLINE_CLUBS = {
        "usm alger": {"id": 9001, "name": "USM Alger", "logo": "https://media.api-sports.io/football/teams/965.png", "country": "Algérie", "division": "Ligue 1"},
        "mc alger": {"id": 9002, "name": "MC Alger", "logo": "https://media.api-sports.io/football/teams/964.png", "country": "Algérie", "division": "Ligue 1"},
        "js kabylie": {"id": 9003, "name": "JS Kabylie", "logo": "https://media.api-sports.io/football/teams/972.png", "country": "Algérie", "division": "Ligue 1"},
        "cr belouizdad": {"id": 9004, "name": "CR Belouizdad", "logo": "https://media.api-sports.io/football/teams/966.png", "country": "Algérie", "division": "Ligue 1"},
        "mc oran": {"id": 9005, "name": "MC Oran", "logo": "https://media.api-sports.io/football/teams/970.png", "country": "Algérie", "division": "Ligue 1"},
        "cs constantine": {"id": 9006, "name": "CS Constantine", "logo": "https://media.api-sports.io/football/teams/968.png", "country": "Algérie", "division": "Ligue 1"},
        "es setif": {"id": 9007, "name": "ES Sétif", "logo": "https://media.api-sports.io/football/teams/967.png", "country": "Algérie", "division": "Ligue 1"},
        "paradou ac": {"id": 9008, "name": "Paradou AC", "logo": "https://media.api-sports.io/football/teams/976.png", "country": "Algérie", "division": "Ligue 1"},
        "paris saint germain": {"id": 9009, "name": "Paris Saint Germain", "logo": "https://media.api-sports.io/football/teams/85.png", "country": "France", "division": "Ligue 1"},
        "marseille": {"id": 9010, "name": "Marseille", "logo": "https://media.api-sports.io/football/teams/81.png", "country": "France", "division": "Ligue 1"},
        "lyon": {"id": 9011, "name": "Lyon", "logo": "https://media.api-sports.io/football/teams/80.png", "country": "France", "division": "Ligue 1"},
        "barcelona": {"id": 9012, "name": "Barcelona", "logo": "https://media.api-sports.io/football/teams/529.png", "country": "Espagne", "division": "La Liga"},
        "real madrid": {"id": 9013, "name": "Real Madrid", "logo": "https://media.api-sports.io/football/teams/541.png", "country": "Espagne", "division": "La Liga"},
        "liverpool": {"id": 9014, "name": "Liverpool", "logo": "https://media.api-sports.io/football/teams/40.png", "country": "Royaume-Uni", "division": "Premier League"},
        "manchester city": {"id": 9015, "name": "Manchester City", "logo": "https://media.api-sports.io/football/teams/50.png", "country": "Royaume-Uni", "division": "Premier League"},
        "manchester united": {"id": 9016, "name": "Manchester United", "logo": "https://media.api-sports.io/football/teams/33.png", "country": "Royaume-Uni", "division": "Premier League"},
        "raja": {"id": 9017, "name": "Raja Casablanca", "logo": "https://media.api-sports.io/football/teams/982.png", "country": "Maroc", "division": "Botola Pro"},
        "wydad": {"id": 9018, "name": "Wydad AC", "logo": "https://media.api-sports.io/football/teams/983.png", "country": "Maroc", "division": "Botola Pro"},
        "usm": {"id": 9001, "name": "USM Alger", "logo": "https://media.api-sports.io/football/teams/965.png", "country": "Algérie", "division": "Ligue 1"},
    }

    # Match offline database first
    for k, v in OFFLINE_CLUBS.items():
        if query_lower in k or k in query_lower:
            return JsonResponse({'results': [v]})

    if query_lower in ALIASES:
        query = ALIASES[query_lower]

    import re
    # If query contains Arabic characters, translate it to English first
    if re.search(r'[\u0600-\u06FF]', query):
        try:
            trans_url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ar&tl=en&dt=t&q=" + urllib.parse.quote(query)
            trans_req = urllib.request.Request(trans_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(trans_req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    translated = data[0][0][0]
                    if translated:
                        query = translated
        except Exception:
            pass

    api_key = getattr(settings, 'API_FOOTBALL_KEY', None)
    if not api_key:
        return JsonResponse({'error': 'API key not configured'}, status=500)

    url = f"https://v3.football.api-sports.io/teams?search={urllib.parse.quote(query)}"
    req = urllib.request.Request(url)
    req.add_header('x-rapidapi-host', 'v3.football.api-sports.io')
    req.add_header('x-rapidapi-key', api_key)
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                teams = data.get('response', [])
                
                if not teams:
                    return JsonResponse({'results': []})
                
                COUNTRY_MAP = {
                    "England": "Royaume-Uni", "Spain": "Espagne", "Italy": "Italie",
                    "Germany": "Allemagne", "Algeria": "Algérie", "Netherlands": "Pays-Bas",
                    "Belgium": "Belgique", "Brazil": "Brésil", "Argentina": "Argentine",
                    "Morocco": "Maroc", "Tunisia": "Tunisie", "Egypt": "Égypte",
                    "Turkey": "Turquie", "Russia": "Russie", "Switzerland": "Suisse",
                    "Scotland": "Royaume-Uni", "Wales": "Royaume-Uni", "Sweden": "Suède",
                    "Denmark": "Danemark", "Norway": "Norvège", "Finland": "Finlande",
                    "Poland": "Pologne", "Austria": "Autriche", "Greece": "Grèce",
                    "Croatia": "Croatie", "Serbia": "Serbie", "Czech Republic": "République Tchèque",
                    "Romania": "Roumanie", "Bulgaria": "Bulgarie", "Hungary": "Hongrie",
                    "Ireland": "Irlande", "USA": "États-Unis", "Mexico": "Mexique",
                    "Colombia": "Colombie", "Chile": "Chili", "Peru": "Pérou",
                    "Saudi Arabia": "Arabie Saoudite", "Qatar": "Qatar",
                    "United Arab Emirates": "Émirats Arabes Unis", "Japan": "Japon",
                    "South Korea": "Corée du Sud", "China": "Chine", "Australia": "Australie",
                    "Ivory Coast": "Côte d'Ivoire", "Senegal": "Sénégal", "Cameroon": "Cameroun",
                    "Nigeria": "Nigeria", "Ghana": "Ghana", "Mali": "Mali",
                    "South Africa": "Afrique du Sud"
                }
                
                formatted_results = []
                for item in teams:
                    team = item.get('team', {})
                    team_name = team.get('name', '')
                    
                    # Filter out youth teams (U21, U19, U23, etc.)
                    if re.search(r'\bu\d{2}\b', team_name.lower()):
                        continue

                    en_country = team.get('country', '')
                    fr_country = COUNTRY_MAP.get(en_country, en_country)
                        
                    formatted_results.append({
                        "id": team.get('id'),
                        "name": team_name,
                        "logo": team.get('logo'),
                        "country": fr_country,
                        "division": ""  # Fetched separately if needed
                    })
                return JsonResponse({'results': formatted_results})
            else:
                return JsonResponse({'error': 'API Error'}, status=response.status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_team_division_api(request):
    """
    Fetches the current league/division for a specific team from API-Football.
    """
    team_id = request.GET.get('team_id')
    if not team_id:
        return JsonResponse({'error': 'Missing team_id'}, status=400)

    api_key = getattr(settings, 'API_FOOTBALL_KEY', None)
    if not api_key:
        return JsonResponse({'error': 'API key not configured'}, status=500)

    url = f"https://v3.football.api-sports.io/leagues?team={team_id}&current=true"
    req = urllib.request.Request(url)
    req.add_header('x-rapidapi-host', 'v3.football.api-sports.io')
    req.add_header('x-rapidapi-key', api_key)

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                leagues = data.get('response', [])
                
                # Exclude cups/internationals if possible, or just take the first one
                # Usually domestic league is first or marked somehow, but we'll take the first available league
                division = ""
                for l in leagues:
                    league_info = l.get('league', {})
                    if league_info.get('type') == 'League':
                        division = league_info.get('name', '')
                        break
                
                if not division and leagues:
                    # fallback to the first returned if no 'League' type is found
                    division = leagues[0].get('league', {}).get('name', '')

                return JsonResponse({'division': division})
            else:
                return JsonResponse({'error': 'API Error'}, status=response.status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
