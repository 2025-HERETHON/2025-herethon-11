from django.urls import path
from . import views  # 또는 views.liked_views로 모듈 분리했다면 거기서 import

urlpatterns = [
    path('mypage/', views.fit_result, name='mypage'),
    path('likes/', views.liked_products, name='liked_products'),
    path('body-size/', views.body_input_view, name='body_input'),
    path('size-check-cup/', views.size_check_cup, name='size_check_cup'),
    path('size-check-pelvis/', views.size_check_pelvis, name='size_check_pelvis'),
    path('save-body-info/', views.save_body_info, name='save_body_info'),
    path('update-profile', views.update_profile, name='update-profile'),
]