# userProfile/apps.py
from django.apps import AppConfig

class UserprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userProfile'

    def ready(self):
        import userProfile.signals  # 🔥 이 줄 추가!
