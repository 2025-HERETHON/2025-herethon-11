from django.urls import path
from . import views  # 또는 views.liked_views로 모듈 분리했다면 거기서 import

urlpatterns = [
    path('likes/', views.liked_products, name='liked_products'),
]
