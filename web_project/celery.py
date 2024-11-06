# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Utilise les paramètres de configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')

app = Celery('web_project')

# Charge les configurations Celery depuis settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découvre automatiquement les tâches définies dans toutes les applications Django
app.autodiscover_tasks()
