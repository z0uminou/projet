import os
import subprocess

class TemperatureSensorManager:
    def __init__(self, directory='/sys/bus/w1/devices', filename='temperature', sensor_name_file='name'):
        self.directory = directory
        self.filename = filename
        self.sensor_name_file = sensor_name_file

    def find_folders_starting_with_28(self):
        """Trouve tous les dossiers dans le répertoire spécifié commençant par '28'."""
        folders = []
        for item in os.listdir(self.directory):
            if os.path.isdir(os.path.join(self.directory, item)) and item.startswith('28'):
                folders.append(os.path.join(self.directory, item))  # Chemin complet du dossier
        return folders

    def read_file_with_cat(self, file_path):
        """Lit le contenu d'un fichier en utilisant la commande `cat`."""
        try:
            result = subprocess.run(['cat', file_path], stdout=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except Exception as e:
            return f"Erreur lors de l'exécution de cat sur {file_path} : {e}"

    def get_sensor_names(self):
        """Renvoie une liste des noms des capteurs présents dans les dossiers commençant par '28'."""
        sensor_names = []
        folders = self.find_folders_starting_with_28()
        
        for folder in folders:
            name_file_path = os.path.join(folder, self.sensor_name_file)
            
            if os.path.exists(name_file_path):
                sensor_name = self.read_file_with_cat(name_file_path)
                sensor_names.append(sensor_name)
                print(f"Nom du capteur trouvé : {sensor_name}")
            else:
                print(f"Le fichier {self.sensor_name_file} n'existe pas dans le dossier {folder}")
        
        return sensor_names

    def get_temperatures(self):
        """Récupère les relevés de température et les noms des capteurs."""
        temperatures = []
        folders = self.find_folders_starting_with_28()
        
        for folder in folders:
            temp_file_path = os.path.join(folder, self.filename)
            name_file_path = os.path.join(folder, self.sensor_name_file)

            if os.path.exists(temp_file_path):
                temperature_raw = self.read_file_with_cat(temp_file_path)
                try:
                    temperature = int(temperature_raw) / 1000  # Conversion en Celsius
                    sensor_name = self.read_file_with_cat(name_file_path)
                    temperatures.append((sensor_name, temperature))
                    #print(f"Contenu du capteur {sensor_name} : {temperature}°C")
                except ValueError:
                    print(f"Erreur de conversion de la température pour le capteur dans {folder}")
            else:
                print(f"Le fichier {self.filename} n'existe pas dans le dossier {folder}")
        
        return temperatures

# Exemple d'utilisation
#sensor_manager = TemperatureSensorManager()
#sensor_names = sensor_manager.get_sensor_names()
