from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product, WornProduct
from .utils import calculate_bust_size, calculate_pelvis_size
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#나의 서랍(프로필 정보, 착용한 제품)
@login_required
def fit_result(request):
    user = request.user

    try:
        profile_image = user.userprofile.profile_image
        nickname = user.userprofile.nickname
    except UserProfile.DoesNotExist: #프로필/닉네임 설정 안했을 때 
        profile_image = None
        nickname = user.username

     #착용한 상품 목록
    worn_products = WornProduct.objects.select_related('product').filter(user=request.user)
    # 착용한 상품 개수
    worn_product_count = worn_products.count()

    context = {
        'user' : user,
        'profile_image' : profile_image,
        'nickname' : nickname,
        'worn_product_count': worn_product_count,
        'worn_products': worn_products,
    }
    return render(request, 'userProfile/fit_result.html', context)

#위시리스트 페이지(프로필 정보)
@login_required
def wish_list(request):
    user = request.user

    try:
        profile_image = user.userprofile.profile_image
        nickname = user.userprofile.nickname
    except UserProfile.DoesNotExist:
        profile_image = None
        nickname = user.username

    context = {
        'user': user,
        'profile_image': profile_image,
        'nickname': nickname,
    }
    return render(request, 'userProfile/wishlist.html', context)

#프로필 수정
@login_required
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user) 

    if request.method == 'POST':
        nickname = request.POST.get('nickname', '').strip()
        profile_image = request.FILES.get('profile_image')

        if nickname:
            profile.nickname = nickname
        if profile_image:
            profile.profile_image = profile_image
        profile.save()

        # 수정 후 돌아갈 경로 설정
        next_url = request.POST.get('next', 'mypage')
        return redirect(next_url)

    context = {
        'nickname': profile.nickname,
        'profile_image': profile.profile_image,
    }
    return render(request, 'userProfile/fit_result.html', context)

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
    # 이미 작성한 체형 사이즈 정보 있는지 확인
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        userprofile = None

    context = {
        'userprofile': userprofile
    }

    return render(request, 'userProfile/body_input.html', context)

#입력한 체형 데이터
def body_size(request):
    # 이미 작성한 체형 사이즈 정보 있는지 확인
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        userprofile = None
    
    if request.method == "POST":
        # 폼에서 값 받기
        is_manual_cup = request.POST.get('is_manual_cup') == 'on'
        is_manual_pelvis = request.POST.get('is_manual_pelvis') == 'on'
        bust = request.POST.get('bust')
        underbust = request.POST.get('underbust')
        cup_size = request.POST.get('cup_size')
        waist = request.POST.get('waist')
        hip = request.POST.get('hip')
        pelvis_size = request.POST.get('pelvis_size')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        is_public = request.POST.get('is_public') == 'on'

        if userprofile:
            userprofile.is_manual_cup = is_manual_cup
            userprofile.is_manual_pelvis = is_manual_pelvis
            userprofile.bust = bust
            userprofile.underbust = underbust
            userprofile.cup_size = cup_size
            userprofile.waist = waist
            userprofile.hip = hip
            userprofile.pelvis_size = pelvis_size
            userprofile.height = height
            userprofile.weight = weight
            userprofile.is_public = is_public
            userprofile.save()
        else:
            UserProfile.objects.create(
                user=request.user,
                is_manual_cup=is_manual_cup,
                is_manual_pelvis=is_manual_pelvis,
                bust=bust,
                underbust=underbust,
                cup_size=cup_size,
                waist=waist,
                hip=hip,
                pelvis_size=pelvis_size,
                height=height,
                weight=weight,
                is_public=is_public,
            )

        return JsonResponse({'message': '저장 완료'})

    # GET 요청일 때 JSON 응답으로 사용자 정보 전달
    if userprofile:
        # pelvis_size는 userprofile.pelvis_size로 가져오도록 수정
        return JsonResponse({
            'is_manual_cup': userprofile.is_manual_cup,
            'is_manual_pelvis': userprofile.is_manual_pelvis,
            'bust': userprofile.bust,
            'underbust': userprofile.underbust,
            'cup_size': userprofile.cup_size,
            'pelvis_size': userprofile.pelvis_size,  # 수정: userprofile.pelvis_size로 가져오기
            'waist': userprofile.waist,
            'hip': userprofile.hip,
            'height': userprofile.height,
            'weight': userprofile.weight,
            'is_public': userprofile.is_public,
        })
    
    return JsonResponse({'message': '사용자 정보 없음'})



#체형 사이즈 측정
#가슴 사이즈 츨정
@csrf_exempt
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
@csrf_exempt
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
@csrf_exempt
@login_required
def save_body_info(request):
    if request.method == "POST":
        try:
            # POST 데이터 가져오기
            data = json.loads(request.body)

            # 각 필드의 값을 가져오고 기본값 처리
            bust = data.get("bust", None)
            underbust = data.get("underbust", None)
            cup_size = data.get("cup_size", "")
            waist = data.get("waist", None)
            hip = data.get("hip", None)
            pelvis_size = data.get("pelvis_size", "")
            height = data.get("height", None)
            weight = data.get("weight", None)
            is_manual_cup = data.get('is_manual_cup', False)  # 기본값 False
            is_manual_pelvis = data.get('is_manual_pelvis', False)  # 기본값 False

            # 현재 로그인한 사용자의 프로필 가져오기 (없으면 새로 생성)
            profile, created = UserProfile.objects.get_or_create(user=request.user)

            # 값이 없으면 None이 아닌 기본값으로 채우기
            profile.bust = bust if bust is not None else None
            profile.underbust = underbust if underbust is not None else None
            profile.cup_size = cup_size or None  # 비어 있으면 None
            profile.waist = waist if waist is not None else None
            profile.hip = hip if hip is not None else None
            profile.pelvis_size = pelvis_size or None  # 비어 있으면 None
            profile.height = height if height is not None else None
            profile.weight = weight if weight is not None else None
            profile.is_manual_cup = is_manual_cup
            profile.is_manual_pelvis = is_manual_pelvis

            # 프로필 저장
            profile.save()

            return JsonResponse({"message": "저장 완료"}, status=200)

        except Exception as e:
            # 오류 발생 시 JSON 응답으로 오류 메시지 반환
            return JsonResponse({"error": str(e)}, status=400)