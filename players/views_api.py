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
