from django.shortcuts import render
from django.db.models import Count
from .models import Product
from review.models import Review
from userProfile.models import UserProfile

# Create your views here.
# 추천 상품 반환
def recommand(request):
    return render(request, 'products/recommand.html')

#상품에 대한 모든 리뷰
def product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    #해당 상품 리뷰들 
    reviews = Review.objects.filter(product=product)\
    .select_related('user', 'user__userprofile')\
    .prefetch_related('liked_users')\
    .order_by('-created_at')
    total_reviews = reviews.count()

    #별점 분포 - [{'rating': 5, 'count': 10}, {'rating':4, 'count':5}, ...]
    rating_distribution = reviews.values('rating').annotate(count=Count('rating'))

    #사이즈 느낌 분포
    size_feel_distribution = reviews.values('size_feel').annotate(count=Count('size_feel'))

    #사이즈 느낌 %로 변환
    size_feel_percent={}
    for item in size_feel_distribution:
        size_feel_percent[item['size_feel']] = round(item['count'] / total_reviews * 100, 1) if total_reviews > 0 else 0
    
    #만족도 텍스트로
    satisfaction_text = dict(Review.SATISFACTION_CHOICES)
    size_feel_text = dict(Review.SIZE_FEEL_CHOICES)

    context = {
        'product': product,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'rating_distribution': rating_distribution,
        'size_feel_percent': size_feel_percent,
        'satisfaction_text': satisfaction_text,
        'size_feel_text': size_feel_text,
    }
    return render(request, 'product/products_review.html', context)