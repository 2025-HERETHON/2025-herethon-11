# userProfile/apps.py

from django.apps import AppConfig
from django.conf import settings

class UserprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userProfile'

    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError
        from django.core.exceptions import ImproperlyConfigured

        try:
            from allauth.socialaccount.models import SocialApp
            from django.contrib.sites.models import Site

            if not SocialApp.objects.filter(provider='google').exists():
                site = Site.objects.get(id=settings.SITE_ID)

                app = SocialApp.objects.create(
                    provider='google',
                    name='Google',
                    client_id=settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID,
                    secret=settings.SOCIAL_AUTH_GOOGLE_SECRET,
                )
                app.sites.add(site)

            if not SocialApp.objects.filter(provider='kakao').exists():
                site = Site.objects.get(id=settings.SITE_ID)

                app = SocialApp.objects.create(
                    provider='kakao',
                    name='Kakao',
                    client_id=settings.SOCIAL_AUTH_KAKAO_CLIENT_ID,
                    secret=settings.SOCIAL_AUTH_KAKAO_SECRET,
                )

                app.sites.add(site)

        except (OperationalError, ProgrammingError, ImproperlyConfigured):
            # 아직 migrate 안됐거나 db 준비 안됐을 경우 무시
            pass
