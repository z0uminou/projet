from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .TensorManagement import TemperatureSensorManager
from .models import Rucher, Ruche, Mesure
import time  # pour la simulation du délai de mesure
from django.http import JsonResponse
from django.urls import reverse
from .weather_service import get_weather_data
import random


# Create your views here.

def home(request):
    return HttpResponse("Hellow, Django !")

#@login_required
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
            'url': reverse('vue_rucher', args=[rucher.id])
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
        'mesures': mesures
    })

def apimeteo(request):
    return render(request, 'weather.html')


def get_weather_data(request):
    data = {
        'temperature': round(random.uniform(15,30),2),
        'humidity': round(random.uniform(40,80),2),
        'status': 'Sunny'
    }
    return JsonResponse(data)

#print("Noms des capteurs:", sensor_names)

"""
def get_sensor_data():
    sensor_data = TemperatureSensorManager()
    get_data = sensor_data.get_temperatures()# Remplacez par votre code de récupération des données 1-wire
    return get_data  # Exemple : température en °C

#def record_temperature(request):
    if request.user.is_authenticated:
        hive_id = request.GET.get('hive_id')
        temperature = get_sensor_data()
        TemperatureReading.objects.create(hive_id=hive_id, temperature=temperature)
        return JsonResponse({'status': 'success', 'temperature': temperature})
    return JsonResponse({'status': 'error', 'message': 'User not authenticated'})
"""