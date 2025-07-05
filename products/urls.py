# products/urls.py
from django.urls import path
from .views.home_views import home

urlpatterns = [
    path('', home, name='home'),  # 이게 있어야 / 로 접속할 수 있어
]
