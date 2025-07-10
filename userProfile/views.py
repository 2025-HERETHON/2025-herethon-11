from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import UserProfile

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product
from .models import UserProfile
from .utils import calculate_bust_size, calculate_pelvis_size

#나의 서랍 
def fit_result(request):
    return render(request, 'userProfile/fit_result.html')

@login_required
def liked_products(request):
    user = request.user
    liked_items = user.liked_products.all()  # Product.liked_users의 related_name

    context = {
        'user_name': user.username,
        'liked_items': liked_items,
    }
    return render(request, 'userProfile/userProfile.html', context)

#body_input.html render
def body_input_view(request):
    return render(request, 'userProfile/body_input.html')

#체형 사이즈 측정
#가슴 사이즈 츨정
@login_required
def size_check_cup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bust = int(data.get('bust'))
        underbust = int(data.get('underbust'))
        cup_size = calculate_bust_size(bust, underbust)
        return JsonResponse({'cup_size': cup_size})
    return JsonResponse({'error': 'POST 요청만 허용'}, status=405)

#골반 사이즈 측정
@login_required
def size_check_pelvis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        waist = int(data.get('waist'))
        hip = int(data.get('hip'))
        pelvis_size = calculate_pelvis_size(waist, hip)
        return JsonResponse({'pelvis_size': pelvis_size})
    return JsonResponse({'error': 'POST 요청만 허용'}, status=405)

def to_int(v):
    try:
        return int(v) if v is not None else None
    except (ValueError, TypeError):
        return None
        
#체형 사이즈 저장
@login_required
def save_body_info(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            bust = to_int(data.get("bust"))
            underbust = to_int(data.get("underbust"))
            cup_size = data.get("cup_size")
            waist = to_int(data.get("waist"))
            hip = to_int(data.get("hip"))
            pelvis_size = data.get("pelvis_size")
            height = to_int(data.get("height"))
            weight = to_int(data.get("weight"))

            # 현재 로그인한 사용자의 프로필 가져오기
            profile, _ = UserProfile.objects.get_or_create(user=request.user)

            # 값 저장
            profile.bust = bust
            profile.underbust = underbust
            profile.cup_size = cup_size
            profile.waist = waist
            profile.hip = hip
            profile.pelvis_size = pelvis_size
            profile.height = height
            profile.weight = weight
            profile.save()

            return JsonResponse({"message": "저장 완료"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)