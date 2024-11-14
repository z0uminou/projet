from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .TensorManagement import TemperatureSensorManager
from .models import Rucher, Ruche, Mesure
import time  # pour la simulation du délai de mesure
from django.http import JsonResponse
from django.urls import reverse
import requests
from django.conf import settings

# Create your views here.

def home(request):
    return HttpResponse("Hellow, Django !")

# @login_required
"""def dashboard(request):
    # Récupérer les relevés de température pour l'utilisateur
    readings = Rucher.objects.filter(nom="Nom des ruchers")
    return render(request, 'dashboard.html', {'readings': readings})
"""

@login_required
def dashboard(request):
    ruchers = Rucher.objects.all()
    ruchers_data = [
        {
            'nom': rucher.nom,
            'latitude': rucher.latitude,
            'longitude': rucher.longitude,
            'url': reverse('vue_rucher', args=[rucher.id])  # reversed URL is only needed here
        }
        for rucher in ruchers
    ]
    return render(request, 'carte.html', {'ruchers': ruchers_data})


def vue_rucher(request, rucher_id):
    rucher = get_object_or_404(Rucher, pk=rucher_id)
    ruches = rucher.ruches.all()  # Liste des ruches dans le rucher
    
    # Si une ruche spécifique est sélectionnée, récupérer ses mesures
    ruche_id = request.GET.get('ruche_id')
    mesures = None
    ruche_select = None
    if ruche_id:
        ruche_select = get_object_or_404(Ruche, pk=ruche_id, rucher=rucher)
        mesures = Mesure.objects.filter(id_capteur__ligne__cadre__ruche=ruche_select)

    return render(request, 'details_rucher.html', {
        'rucher': rucher,
        'ruches': ruches,
        'ruche_select': ruche_select,
        'mesures': mesures,
    })


def apimeteo(station_id, start_date, end_date):
    url = f"https://exemple.com/api/releve/{station_id}"
    headers = {
        'Authorization': f'Bearer {settings.API_TOKEN}'  # Utilisez le token API configuré dans settings.py
    }
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.get(url, headers=headers, params=params)
    
    # Vérifier la réponse de l'API
    if response.status_code == 200:
        return response.json()  # Renvoie les données au format JSON
    else:
        return None

def releve_data(request):
    if request.method == 'POST':
        station_id = request.POST['station_id']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        
        # Appel de l'API pour récupérer les données
        data = apimeteo(station_id, start_date, end_date)  # use the function here

        # Vérifier si des données ont été renvoyées
        if data:
            return render(request, 'apimeteo.html', {'data': data})
        else:
            return render(request, 'apimeteo.html', {'error': 'Aucune donnée trouvée pour cette période.'})

    return render(request, 'apimeteo.html')
