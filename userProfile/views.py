from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product

@login_required
def liked_products(request):
    user = request.user
    liked_items = user.liked_products.all()  # Product.liked_users의 related_name

    context = {
        'user_name': user.username,
        'liked_items': liked_items,
    }
    return render(request, 'userProfile/userProfile.html', context)
