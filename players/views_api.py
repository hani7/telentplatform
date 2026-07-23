import requests
from django.http import JsonResponse
from django.conf import settings

def search_clubs_api(request):
    """
    Proxy view for searching football clubs via API-Sports (API-Football).
    Requires API_FOOTBALL_KEY in settings or environment.
    If no key is present, returns a fallback mock list for demonstration.
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})

    # Retrieve API key from settings (you should add this to your .env)
    api_key = getattr(settings, 'API_FOOTBALL_KEY', None)

    if not api_key:
        # Fallback / Mock mode if API key is not yet configured
        # To make it feel real during tests, we return some dummy data based on the query
        mock_db = [
            {"name": "Real Madrid", "logo": "https://media.api-sports.io/football/teams/541.png", "country": "Spain"},
            {"name": "FC Barcelona", "logo": "https://media.api-sports.io/football/teams/529.png", "country": "Spain"},
            {"name": "Paris Saint-Germain", "logo": "https://media.api-sports.io/football/teams/85.png", "country": "France"},
            {"name": "Manchester United", "logo": "https://media.api-sports.io/football/teams/33.png", "country": "England"},
            {"name": "Manchester City", "logo": "https://media.api-sports.io/football/teams/50.png", "country": "England"},
            {"name": "Arsenal", "logo": "https://media.api-sports.io/football/teams/42.png", "country": "England"},
            {"name": "Bayern Munich", "logo": "https://media.api-sports.io/football/teams/157.png", "country": "Germany"},
            {"name": "Juventus", "logo": "https://media.api-sports.io/football/teams/496.png", "country": "Italy"},
            {"name": "AC Milan", "logo": "https://media.api-sports.io/football/teams/489.png", "country": "Italy"},
            {"name": "Inter Milan", "logo": "https://media.api-sports.io/football/teams/505.png", "country": "Italy"},
            {"name": "Mouloudia d'Alger (MCA)", "logo": "", "country": "Algeria"},
            {"name": "CR Belouizdad", "logo": "", "country": "Algeria"},
            {"name": "USM Alger", "logo": "", "country": "Algeria"},
            {"name": "JS Kabylie", "logo": "", "country": "Algeria"},
        ]
        results = [c for c in mock_db if query.lower() in c['name'].lower()]
        return JsonResponse({'results': results})

    # Real API Call
    url = "https://v3.football.api-sports.io/teams"
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_key
    }
    try:
        response = requests.get(url, headers=headers, params={'search': query})
        if response.status_code == 200:
            data = response.json()
            teams = data.get('response', [])
            formatted_results = []
            for item in teams:
                team = item.get('team', {})
                formatted_results.append({
                    "name": team.get('name'),
                    "logo": team.get('logo'),
                    "country": team.get('country')
                })
            return JsonResponse({'results': formatted_results})
        else:
            return JsonResponse({'error': 'API Error'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
