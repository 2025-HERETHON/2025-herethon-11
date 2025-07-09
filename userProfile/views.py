from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product, WornProduct

@login_required
def liked_products(request):
    user = request.user
    liked_items = user.liked_products.all()  # Product.liked_users의 related_name

    context = {
        'user_name': user.username,
        'liked_items': liked_items,
    }
    return render(request, 'userProfile/userProfile.html', context)


@login_required
def user_profile_view(request):  # 함수 이름 변경
    user = request.user
    liked_items = user.liked_products.all()
    worn_products = WornProduct.objects.filter(user=user).select_related('product')

    return render(request, 'userProfile/userProfile.html', {
        'user_name': user.username,
        'liked_items': liked_items,
        'worn_products': worn_products,
    })