# products/views/like_views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Product
from django.shortcuts import redirect

@login_required
def toggle_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if user in product.liked_users.all():
        product.liked_users.remove(user)
        print(f"{user.username} UNLIKED {product.title}")
    else:
        product.liked_users.add(user)
        print(f"{user.username} LIKED {product.title}")

    return redirect('home')  # ✅ 홈 페이지로 리다이렉트


