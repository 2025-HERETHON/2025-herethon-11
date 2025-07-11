from django.shortcuts import get_object_or_404, render
from products.models import Product, RecentlyViewedProduct, WornProduct
from django.utils import timezone
from review.models import Review
from django.db.models import Count

def product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # 좋아요 개수 기준으로 리뷰 정렬
    reviews = (
        Review.objects
        .filter(product=product)
        .annotate(like_count=Count('like_users'))
        .order_by('-like_count', '-created_at')  # 좋아요 많은 순 + 최신순
    )

    # 착용 정보 붙이기
    for review in reviews:
        try:
            worn = WornProduct.objects.get(user=review.user, product=product)
            review.worn_color = worn.color
            review.worn_size = worn.size
        except WornProduct.DoesNotExist:
            review.worn_color = None
            review.worn_size = None

    total_reviews = reviews.count()
    satisfied_count = sum(review.like_users.count() for review in reviews)

    return render(request, 'products/product_review.html', {
        'product': product,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'satisfied_count': satisfied_count,
    })


