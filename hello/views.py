from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .TensorManagement import TemperatureSensorManager
from .models import Rucher
import time  # pour la simulation du délai de mesure
from django.http import JsonResponse



# Create your views here.

def home(request):
    return HttpResponse("Hellow, Django !")

@login_required
def dashboard(request):
    # Récupérer les relevés de température pour l'utilisateur
    readings = Rucher.objects.filter(nom="Nom des ruchers")
    return render(request, 'dashboard.html', {'readings': readings})

@login_required
def carte_view(request):
    return render(request, 'carte.html')


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