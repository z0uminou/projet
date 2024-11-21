from celery import shared_task
from .models import Mesure, Capteur
from .TensorManagement import TemperatureSensorManager


"""
def record_temperature(hive_id):
    sensor_manager = TemperatureSensorManager()
    temperatures = sensor_manager.get_temperatures()  # Obtenir les températures
    
    for sensor_name, temperature in temperatures:
        Mesure.objects.create(hive_id=hive_id, id_capteur= sensor_name, temperature=temperature)

"""

@shared_task
def enregistrer_mesure():
    # Récupérez l'instance de Capteur en fonction de l'identifiant
    sensor_manager = TemperatureSensorManager()
    temperatures = sensor_manager.get_temperatures()
    for sensor_name, temperature in temperatures:
        capteur = Capteur.objects.get(identifiant= sensor_name)
        # Créez la mesure en liant le capteur
        Mesure.objects.create(id_capteur=capteur, temperature=temperature)
    print(f"Mesure enregistrée pour le capteur {capteur.identifiant}: {temperature}°C")
    return "Enregistrement terminé pour tous les capteurs disponibles."

