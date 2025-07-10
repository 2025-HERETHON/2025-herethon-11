# views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from products.models import Product


@login_required
def toggle_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.liked_users.all():
        product.liked_users.remove(request.user)
        return JsonResponse({'status': 'unliked'})
    else:
        product.liked_users.add(request.user)
        return JsonResponse({'status': 'liked'})
