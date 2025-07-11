# views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from products.models import Product, WornProduct
from products.views.home_views import expand_sizes
from userProfile.models import UserProfile


@login_required
def toggle_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.liked_users.all():
        product.liked_users.remove(request.user)
        return JsonResponse({'status': 'unliked'})
    else:
        product.liked_users.add(request.user)
        return JsonResponse({'status': 'liked'})


def search_filter(request):
    query = request.GET.get('q', '').strip()
    colors = [c.strip() for c in request.GET.getlist('color')]
    materials = [m.strip().lower() for m in request.GET.getlist('material')]
    types = request.GET.getlist("type")
    bra_size = request.GET.get("bra_size")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    products = Product.objects.all()

    if query:
        products = products.filter(title__icontains=query)

    if colors:
        color_q = Q()
        for color in colors:
            color_q |= Q(color__icontains=color)
        products = products.filter(color_q)

    if materials:
        matched_ids = []
        for p in products:
            raw = p.material.replace(",", " ")
            product_mats = [m.strip().lower() for m in raw.split() if m.strip()]
            if any(mat in product_mats for mat in materials):
                matched_ids.append(p.id)
        products = products.filter(id__in=matched_ids)

    if types:
        products = products.filter(
            Q(categories__name__in=types) |
            Q(subcategories__name__in=types)
        ).distinct()

    # 🔻🔻🔻 체형 기반 필터링 시작 🔻🔻🔻
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass

    body_loaded = request.GET.get("body_loaded")
    if body_loaded == "1":
        request.session["body_loaded"] = True
    elif body_loaded == "0":
        request.session["body_loaded"] = False

    is_body_loaded = request.session.get("body_loaded", False)

    if not bra_size and user_profile and user_profile.cup_size:
        bra_size = user_profile.cup_size.strip()

    bra_matched_ids = set()
    panty_matched_ids = set()

    if is_body_loaded:
        # 브라 필터
        if bra_size:
            for product in products:
                if product.categories.filter(name="브래지어").exists():
                    if bra_size in expand_sizes(product.size):
                        bra_matched_ids.add(product.id)

        # 팬티 필터
        if user_profile and user_profile.pelvis_size:
            import re
            match = re.match(r"([A-Z]+)", user_profile.pelvis_size.strip())
            if match:
                hip_size_code = match.group(1)
                for product in products:
                    if product.categories.filter(name="팬티").exists():
                        if product.size and hip_size_code in product.size:
                            panty_matched_ids.add(product.id)

        if bra_matched_ids or panty_matched_ids:
            matched_ids = bra_matched_ids.union(panty_matched_ids)
            products = products.filter(id__in=matched_ids)
    # 🔺🔺🔺 체형 기반 필터링 끝 🔺🔺🔺

    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass

    return render(request, 'products/product_search.html', {
        'query': query,
        'products': products,
        'selected_colors': colors,
        'selected_materials': materials,
        'selected_types': types,
    })


@login_required
def get_user_body_info(request):
    user = request.user
    try:
        profile = user.userprofile
        return JsonResponse({
            "height": profile.height,
            "weight": profile.weight,
            "cup_size": profile.cup_size,
            "pelvis_size": profile.pelvis_size
        })
    except:
        return JsonResponse({"error": "프로필 없음"}, status=404)