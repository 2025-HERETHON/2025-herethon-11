from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from products.models import Product, WornProduct, RecentlyViewedProduct
import re

# 컵 조합을 실제 사이즈 리스트로 확장하는 함수
def expand_sizes(size_string):
    if not size_string:
        return []
    sizes = []
    if '/' in size_string:
        for part in size_string.split('/'):
            sizes.extend(expand_sizes(part))
        return sizes
    match = re.match(r"(\d+)([A-Z]+)", size_string)
    if not match:
        return [size_string]
    band, cups = match.groups()
    return [f"{band}{cup}" for cup in cups]


def home(request):
    products = Product.objects.all()

    # 필터 값 받기
    colors = [c.strip() for c in request.GET.getlist("color")]
    materials = [m.strip() for m in request.GET.getlist("material")]
    types = request.GET.getlist("type")
    bra_size = request.GET.get("bra_size")

    print("colors:", colors)
    print("materials:", materials)
    print("types:", types)
    print("bra_size:", bra_size)

    # 색상 필터 (OR 조건)
    if colors:
        color_q = Q()
        for color in colors:
            color_q |= Q(color__icontains=color)
        products = products.filter(color_q)

    # 소재 필터 (AND 조건)
    if materials:
        for mat in materials:
            products = products.filter(material__icontains=mat)

    # 타입(카테고리) 필터
    if types:
        products = products.filter(
            Q(categories__name__in=types) |
            Q(subcategories__name__in=types)
        ).distinct()

    # 브라 사이즈 필터 (브래지어 타입일 때만 적용)
    if "브래지어" in types and bra_size:
        matched = []
        for product in products:
            expanded_sizes = expand_sizes(product.size)
            if bra_size in expanded_sizes:
                matched.append(product.id)
        products = products.filter(id__in=matched)

    # 가격 필터
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

    # 착용한 상품 ID 목록
    worn_product_ids = []
    if request.user.is_authenticated:
        worn_product_ids = list(
            WornProduct.objects
            .filter(user=request.user)
            .values_list("product_id", flat=True)
        )

    # 최근 본 상품
    recent_products = []
    if request.user.is_authenticated:
        recent_products = [
            rv.product for rv in RecentlyViewedProduct.objects
            .filter(user=request.user)
            .select_related('product')
            .order_by('-viewed_at')[:5]
        ]

    print("필터 결과 상품 개수:", products.count())
    print("필터 결과 상품 ID들:", list(products.values_list("id", flat=True)))

    context = {
        "rec_items": products,
        "user_name": request.user.username if request.user.is_authenticated else "비회원",
        "worn_product_ids": worn_product_ids,
        "recent_products": recent_products,
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
    query = request.GET.get('q', '').strip()
    colors = [c.strip() for c in request.GET.getlist('color')]
    materials = [m.strip() for m in request.GET.getlist('material')]
    types = [t.strip() for t in request.GET.getlist('type')]

    products = Product.objects.all()

    # 검색어 필터
    if query:
        products = products.filter(title__icontains=query)

    # 색상 필터 (OR 조건)
    if colors:
        color_q = Q()
        for color in colors:
            color_q |= Q(color__icontains=color)
        products = products.filter(color_q)

    # 소재 필터
    if materials:
        for material in materials:
            products = products.filter(material__icontains=material)

    # 타입(카테고리) 필터 – ManyToManyField(Category)
    if types:
        products = products.filter(categories__name__in=types).distinct()

    return render(request, 'products/product_search.html', {
        'query': query,
        'products': products,
        'selected_colors': colors,
        'selected_materials': materials,
        'selected_types': types,
    })



def wear_modal(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("상품이 존재하지 않습니다.")

    # GET 파라미터에서 colors, sizes 파싱
    colors = request.GET.get("colors", "").split(",")
    sizes = request.GET.get("sizes", "").split(",")

    print("colors raw:", request.GET.get("colors"))  # 한 번 찍어보자
    print("parsed colors:", colors)

    return render(request, "products/option_modal.html", {
        "product": product,
        "colors": colors,
        "sizes": sizes,
    })


