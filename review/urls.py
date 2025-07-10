from django.urls import path
from .views import *

urlpatterns = [
    path('', list_review, name='list_review'),
    path('detail_review/<int:review_id>/', detail_review, name='detail_review'),
    path('create_review/<int:product_id>/', create_review, name='create_review'),
    path('update_review/<int:id>/', update_review, name='update_review'),
    path('delete_review/<int:id>/', delete_review, name='delete_review'),
    path('<int:review_id>/likes/', likes, name='likes'), 
]