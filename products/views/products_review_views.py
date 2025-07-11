# products/views/product_views.py (또는 detail 뷰 위치)
from django.shortcuts import get_object_or_404, render
from products.models import Product, RecentlyViewedProduct
from django.utils import timezone

from review.models import Review


def product_review(request, product_id):
    # 예시 코드
    product = Product.objects.get(id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'products/product_review.html', {
        'product': product,
        'reviews': reviews
    })