import requests

def get_weather_data(lat, lon, api_key):
    """Appel API pour récupérer les données météo."""
    BASE_URL = "https://portail-api.meteofrance.fr/web/fr/api/test/a5935def-80ae-4e7e-83bc-3ef622f0438d/6ac1d31a-fe9d-4d18-9b88-582c26908f09"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
