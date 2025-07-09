# wear_views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product, WornProduct
from django.shortcuts import render

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

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def worn_products_list(request):
    worn_products = WornProduct.objects.filter(user=request.user).select_related('product')
    return render(request, 'userProfile/worn_list.html', {
        'worn_products': worn_products
    })
