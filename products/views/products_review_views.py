from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404
from products.models import Product, WornProduct
from review.models import Review

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

    # 평균 평점 계산
    rating_avg = (
        Review.objects
        .filter(product=product)
        .aggregate(avg_rating=Avg('rating'))['avg_rating']
    )
    rating_avg = round(rating_avg or 0, 1)

    # 사이즈 만족도 퍼센트 계산
    size_counts = {
        'big': reviews.filter(size_feel='big').count(),
        'normal': reviews.filter(size_feel='normal').count(),
        'small': reviews.filter(size_feel='small').count(),
    }
    size_feel_percent = {
        key: round((count / total_reviews) * 100) if total_reviews > 0 else 0
        for key, count in size_counts.items()
    }

    # 별점 breakdown 계산 (5~1점)
    rating_breakdown = Review.objects.filter(product=product).values('rating').annotate(count=Count('id'))

    # 기본값 0으로 초기화
    rating_count = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for entry in rating_breakdown:
        rating_count[entry['rating']] = entry['count']

    # 전체 리뷰 수 기준 비율 계산
    rating_percent = {
        str(star): round((count / total_reviews) * 100) if total_reviews else 0
        for star, count in rating_count.items()
    }

    if rating_percent is None:
        rating_percent = {}

    print("rating_breakdown:", list(rating_breakdown))

    return render(request, 'products/product_review.html', {
        'product': product,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'satisfied_count': satisfied_count,
        'size_feel_percent': size_feel_percent,
        'rating_avg': rating_avg,
        'rating_percent': rating_percent,
    })



