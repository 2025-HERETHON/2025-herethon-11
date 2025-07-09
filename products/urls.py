# products/urls.py
from django.urls import path
from .views import home, toggle_like
from .views.wear_views import toggle_wear
from .views.home_views import product_option_modal
urlpatterns = [
    path('', home, name='home'),
    path('like/<int:product_id>/', toggle_like, name='toggle_like'),
    path('wear/<int:product_id>/', toggle_wear, name='toggle_wear'),
    path('products/<int:product_id>/options/', product_option_modal, name='product_option_modal'),
]


