from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Apiculteur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class Rucher(models.Model):
    apiculteurs = models.ManyToManyField(Apiculteur, related_name="ruchers")
    nom = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)  # Ajouter la latitude
    longitude = models.FloatField(blank=True, null=True)  # Ajouter la longitude
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - ({self.latitude}) : ({self.longitude})"


class Ruche(models.Model):
    rucher = models.ForeignKey(Rucher, on_delete=models.CASCADE, related_name="ruches")
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True, null=True)  # ex : "Dadant", "Langstroth"
    date_installation = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} (Rucher: {self.rucher.nom})"


class Cadre(models.Model):
    ruche = models.ForeignKey(Ruche, on_delete=models.CASCADE, related_name="cadres")
    numero = models.IntegerField()  # Numéro de cadre pour repérer l'emplacement dans la ruche
    
    def __str__(self):
        return f"Cadre {self.numero} (Ruche: {self.ruche.nom})"

class Ligne(models.Model):
    cadre = models.ForeignKey(Cadre,on_delete=models.CASCADE, related_name="Lignes" )
    numero_ligne = models.IntegerField()

    def __str__(self):
        return f"Ligne {self.numero_ligne} (Cadre: {self.cadre.numero})"
    
class Capteur(models.Model):
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE, related_name="capteurs")
    identifiant = models.CharField(max_length=50)  # Identifiant unique du capteur
    position = models.IntegerField() # Position du capteur sur la ligne (1 à 5 par exemple)


    def __str__(self):
        return f"Capteur {self.identifiant} (Position: {self.position},Ligne: {self.ligne.numero_ligne})"
    

class Mesure(models.Model):
    id_capteur = models.ForeignKey(Capteur,on_delete=models.CASCADE, null=True, blank=True, related_name="mesures")
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Date {self.date} Mesure {self.temperature} (Capteur {self.id_capteur}, Position {self.id_capteur.position})"
    
    


