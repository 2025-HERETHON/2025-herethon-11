# products/views/product_views.py (또는 detail 뷰 위치)
from django.shortcuts import get_object_or_404, render
from products.models import Product, RecentlyViewedProduct
from django.utils import timezone

def product_review(request):
    return render(request, 'products/product_review.html')