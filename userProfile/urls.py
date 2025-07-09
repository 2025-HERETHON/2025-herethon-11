from django.urls import path
from userProfile.views import user_profile_view
from products.views.wear_views import worn_products_list

urlpatterns = [
    path('', user_profile_view, name='user_profile'),
]

