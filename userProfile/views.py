from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product
from .utils import calculate_bust_size, calculate_pelvis_size

@login_required
def liked_products(request):
    user = request.user
    liked_items = user.liked_products.all()  # Product.liked_users의 related_name

    context = {
        'user_name': user.username,
        'liked_items': liked_items,
    }
    return render(request, 'userProfile/userProfile.html', context)



#체형 사이즈 측정
def size_check(request):
    result = None

    if request.method == 'POST':
        try:
            bust = float(request.POST.get('bust'))
            underbust = float(request.POST.get('underbust'))
            waist = float(request.POST.get('waist'))
            hip = float(request.POST.get('hip'))

            cup_result = calculate_bust_size(bust, underbust)
            pelvis_result = calculate_pelvis_size(waist, hip)

            result = {
                'cup_size': cup_result,
                'pelvis_size': pelvis_result
            }
        except(TypeError, ValueError):
            result = {"error": "입력값이 잘못되었습니다."}
        
    return render(request, '', {'result': result}) #html만 작성하면 됨