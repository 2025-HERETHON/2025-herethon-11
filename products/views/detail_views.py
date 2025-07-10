# products/views/product_views.py (또는 detail 뷰 위치)
from django.shortcuts import get_object_or_404, render

# products/views/product_views.py (또는 detail 뷰 위치)

from products.models import Product, RecentlyViewedProduct
from django.utils import timezone
from review.models import Review

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        RecentlyViewedProduct.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'viewed_at': timezone.now()}
        )


    colors = product.color.split(',') if product.color else []
    sizes = product.size.split(',') if product.size else []

    review_count = Review.objects.filter(product=product).count()

    satisfaction_good_count = Review.objects.filter(product=product, satisfaction='good').count()

    is_liked = False
    if request.user.is_authenticated:
        is_liked = product.liked_users.filter(id=request.user.id).exists()

    context = {
        'product': product,
        'title': product.title,
        'price': product.price,
        'shop': product.shop,
        'like_count': product.liked_users.count(),
        'colors': colors,
        'sizes': sizes,
        'review_count': review_count,
        'satisfaction_good_count': satisfaction_good_count,
        'images': product.images.all(),
        'is_liked': is_liked,
    }
    return render(request, 'products/products_detail.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Product
from django.shortcuts import redirect


@login_required
def detail_toggle_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if user in product.liked_users.all():
        product.liked_users.remove(user)
        print(f"{user.username} UNLIKED {product.title}")
    else:
        product.liked_users.add(user)
        print(f"{user.username} LIKED {product.title}")

    return redirect('product_detail', product_id=product.id)
