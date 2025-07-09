# products/views/home_views.py

from django.shortcuts import render, get_object_or_404
from products.models import Product, WornProduct
import re


# 컵 조합을 실제 사이즈 리스트로 확장하는 함수
def expand_sizes(size_string):
    """
    예: "80ABC" → ['80A', '80B', '80C']
        "80A"   → ['80A']
        "75A/75B" → ['75A', '75B']
    """
    if not size_string:
        return []

    sizes = []

    # 슬래시로 구분된 경우
    if '/' in size_string:
        for part in size_string.split('/'):
            sizes.extend(expand_sizes(part))
        return sizes

    # 정규식: 숫자 + 알파벳 조합
    match = re.match(r"(\d+)([A-Z]+)", size_string)
    if not match:
        return [size_string]

    band, cups = match.groups()
    return [f"{band}{cup}" for cup in cups]


def home(request):
    products = Product.objects.all()

    # 필터 값 받기
    colors = request.GET.getlist("color")
    materials = request.GET.getlist("material")
    types = request.GET.getlist("type")  # 카테고리 이름
    bra_size = request.GET.get("bra_size")  # 예: 80A

    # 가격 필터 (최소 ~ 최대)
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

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

    # 색상 필터
    if colors:
        products = products.filter(color__in=colors)

    # 소재 필터
    if materials:
        products = products.filter(material__in=materials)

    # 카테고리 필터 (ManyToMany → name 기준)
    if types:
        products = products.filter(categories__name__in=types).distinct()

    # 브라 사이즈 필터 (컵 복합 대응)
    # 카테고리 필터 (ManyToMany → name 기준)
    if types:
        products = products.filter(categories__name__in=types).distinct()

        # 만약 브래지어가 필터에 포함된 경우만 브라 사이즈 필터 적용
        if "브래지어" in types and bra_size:
            matched = []
            for product in products:
                expanded_sizes = expand_sizes(product.size)
                if bra_size in expanded_sizes:
                    matched.append(product.id)
            products = products.filter(id__in=matched)

    # 착용한 상품 ID 목록
    worn_product_ids = []
    if request.user.is_authenticated:
        worn_product_ids = list(WornProduct.objects.filter(user=request.user).values_list("product_id", flat=True))

    context = {
        "rec_items": products,
        "user_name": request.user.username if request.user.is_authenticated else "비회원",
        "worn_product_ids": worn_product_ids,  # 👈 추가된 부분
    }

    return render(request, "products/products.html", context)


# views.py
def product_option_modal(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/option_modal.html", {
        "product": product,
        "colors": product.color.split(","),
        "sizes": product.size.split(","),
    })


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=query) if query else []
    return render(request, 'products/search_results.html', {
        'query': query,
        'products': products
    })