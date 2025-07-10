# products/urls.py
from django.urls import path
from .views import home, toggle_like
from .views.wear_views import toggle_wear
from .views.detail_views import product_detail, detail_toggle_like
from .views.home_views import product_option_modal, product_search
from .views.products_review_views import product_review
urlpatterns = [
    path('', home, name='home'),
    path('like/<int:product_id>/', toggle_like, name='toggle_like'),
    path('wear/<int:product_id>/', toggle_wear, name='toggle_wear'),
    path('products/<int:product_id>/options/', product_option_modal, name='product_option_modal'),
    path('search/', product_search, name='product_search'),
    path('<int:product_id>/', product_detail, name='product_detail'),# 👈 이거!
    path('review/', product_review, name='product_review'),
path('detail-like/<int:product_id>/', detail_toggle_like, name='detail_toggle_like'),  # 상세페이지 전용 토글
]


