from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from products.models import Product, WornProduct, RecentlyViewedProduct
import re
from userProfile.models import UserProfile

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

    print("colors:", colors)
    print("materials:", materials)
    print("types:", types)

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

    # 체형 정보 가져오기
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass

    # 🔻 사이즈 기반 추천 필터링 (브라 + 팬티 합집합)
    matched_ids = set()

    # 🔹 1. 유저가 버튼 눌렀는지 확인
    # 체형 필터 활성화 여부 확인
    body_loaded = request.GET.get("body_loaded")
    if body_loaded == "1":
        request.session["body_loaded"] = True
    elif body_loaded == "0":
        request.session["body_loaded"] = False

    # 세션에서 불러오기
    is_body_loaded = request.session.get("body_loaded", False)

    bra_matched_ids = set()
    panty_matched_ids = set()

    # 🔹 2. 사이즈 데이터 있으면 적용
    bra_size = request.GET.get("bra_size")
    if not bra_size and user_profile and user_profile.cup_size:
        bra_size = user_profile.cup_size.strip()

    if is_body_loaded:
        # 브라
        if bra_size:
            for product in products:
                if product.categories.filter(name="브래지어").exists():
                    if bra_size in expand_sizes(product.size):
                        bra_matched_ids.add(product.id)

        # 팬티
        if user_profile and user_profile.pelvis_size:
            match = re.match(r"([A-Z]+)", user_profile.pelvis_size.strip())
            if match:
                hip_size_code = match.group(1)
                for product in products:
                    if product.categories.filter(name="팬티").exists():
                        if product.size and hip_size_code in product.size:
                            panty_matched_ids.add(product.id)

        # 🔸 브라나 팬티 중 하나라도 만족한 상품 전체 필터링
        matched_ids = bra_matched_ids.union(panty_matched_ids)
        if matched_ids:
            products = products.filter(id__in=matched_ids)

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
        "user_profile": user_profile
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