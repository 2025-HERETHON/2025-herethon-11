# products/urls.py
from django.urls import path
from .views import home, toggle_like  # ← 명확하게 불러오자

urlpatterns = [
    path('', home, name='home'),
    path('like/<int:product_id>/', toggle_like, name='toggle_like'),
]


