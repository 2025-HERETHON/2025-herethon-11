# views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from products.models import Product, WornProduct
from products.views.home_views import expand_sizes


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

    if request.user.is_authenticated:
        worn_products = Product.objects.filter(wornproduct__user=request.user)
    else:
        worn_products = []

    print("이거 설마")
    if query:
        products = products.filter(title__icontains=query)

    if colors:
        color_q = Q()
        for color in colors:
            color_q |= Q(color__icontains=color)
        products = products.filter(color_q)

    if materials:
        print("👉 요청된 materials:", materials)  # ✅ 클라이언트에서 온 소재 목록
        matched_ids = []
        for p in products:
            raw = p.material.replace(",", " ")
            product_mats = [m.strip().lower() for m in raw.split() if m.strip()]
            print(f"[{p.id}] product_mats:", product_mats)  # ✅ 각 상품의 소재 리스트
            if any(mat in product_mats for mat in materials):
                matched_ids.append(p.id)
        print("✅ 최종 matched_ids:", matched_ids)
        products = products.filter(id__in=matched_ids)
    else:
        print("절단")

    if types:
        products = products.filter(
            Q(categories__name__in=types) |
            Q(subcategories__name__in=types)
        ).distinct()

    if "브래지어" in types and bra_size:
        matched = []
        for product in products:
            expanded = expand_sizes(product.size)
            if bra_size in expanded:
                matched.append(product.id)
        products = products.filter(id__in=matched)

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
        "worn_products": worn_products,
    })

@login_required
def toggle_wear(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if request.method == "POST":
        selected_size = request.POST.get("size")
        selected_color = request.POST.get("color")

        try:
            # 해제: 이미 착용된 상태 → 삭제
            worn = WornProduct.objects.get(user=user, product=product)
            worn.delete()
        except WornProduct.DoesNotExist:
            # 등록: 옵션이 전달된 경우에만 저장
            if selected_size and selected_color:
                WornProduct.objects.create(
                    user=user,
                    product=product,
                    size=selected_size,
                    color=selected_color,
                )

    return redirect(request.META.get('HTTP_REFERER', 'search'))

