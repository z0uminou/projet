from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import Rucher, Ruche, Mesure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import base64
import time  # pour la simulation du délai de mesure
import json
from django.db.models import Max

# Page d'accueil simple
def home(request):
    return HttpResponse("Hello, Django!")

# Vue du tableau de bord avec la liste des ruchers
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

# Vue pour afficher les détails d'un rucher et un graphique 3D des mesures
@login_required
def vue_rucher(request, rucher_id):
    rucher = get_object_or_404(Rucher, pk=rucher_id)
    ruches = rucher.ruches.all()  # Liste des ruches dans le rucher
    
    # Si une ruche spécifique est sélectionnée, récupérer ses mesures
    ruche_id = request.GET.get('ruche_id')
    ruche_select = None
    mesure_data = []
   # image_base64 = None  # Variable pour l'image du graphique

    if ruche_id:
        ruche_select = get_object_or_404(Ruche, pk=ruche_id, rucher=rucher)
        
        latest_mesures = (

            Mesure.objects.filter(id_capteur__ligne__cadre__ruche=ruche_select)
            .values('id_capteur')
            .annotate(latest_date=Max('date'))
        )

        capteur_date_pairs = [(m['id_capteur'], m['latest_date']) for m in latest_mesures]

        mesures = Mesure.objects.filter(
            id_capteur__ligne__cadre__ruche=ruche_select,
            id_capteur__in=[pair[0] for pair in capteur_date_pairs],
            date__in=[pair[1] for pair in capteur_date_pairs],

        )

        mesures_data = [
            {
                'capteur_id': mesure.id_capteur.identifiant,
                'temperature': mesure.temperature,
                'ligne': mesure.id_capteur.ligne.numero_ligne,
                'cadre': mesure.id_capteur.ligne.cadre.numero,
                'capteur_position': mesure.id_capteur.position,
            }
            for mesure in mesures
        ]
    



        # for mesure in mesures:
        #     capteur = mesure.id_capteur
        #     mesure_data.append({
        #         "ligne": capteur.ligne.numero_ligne,
        #         "cadre": capteur.ligne.cadre.numero,
        #         "capteur_position": capteur.position,
        #         "temperature": mesure.temperature,
        #         "capteur_id": capteur.identifiant,
        #     })

        # # Préparer les données pour le graphique 3D
        # y = [mesure.id_capteur.ligne.cadre.numero for mesure in mesures]
        # z = [mesure.id_capteur.ligne.numero_ligne for mesure in mesures]
        # x = [mesure.id_capteur.position for mesure in mesures]
        # temperature = [mesure.temperature for mesure in mesures]

        # # Créer le graphique 3D
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # scatter = ax.scatter(x, y, z, c=temperature, cmap='viridis')


        # # Paramétrer les axes
        # ax.set_xlabel('Position du Capteur')
        # ax.set_ylabel('Cadre')
        # ax.set_zlabel('Ligne')
        # ax.set_title(f'Températures des capteurs dans la ruche {ruche_select.nom}')

        # # Sauvegarder le graphique en mémoire et encoder en base64
        # buf = io.BytesIO()
        # plt.savefig(buf, format='png')
        # buf.seek(0)
        # image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        # buf.close()
        # plt.close(fig)  # Fermer la figure pour libérer la mémoire



    # Passer les données au template
    return render(request, 'details_rucher.html', {
        'rucher': rucher,
        'ruches': ruches,
        'ruche_select': ruche_select,
        'mesures_data': mesure_data,
 #       'image_base64': image_base64,
    })

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