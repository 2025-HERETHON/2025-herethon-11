from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product, WornProduct
from .models import Review

# Create your views here.

#리뷰 등록
@login_required
def create_review(request):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        satisfaction = request.POST.get('satisfaction')
        size_feel = request.POST.get('size_feel')
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        content = request.POST.get('content')

        Review.objects.create(
            user=request.user,
            product=product,
            satisfaction=satisfaction,
            size_feel=size_feel,
            rating=rating,
            title=title,
            content=content,
        )
        return redirect('list_review') #리뷰 작성 후 목록 페이지로 이동
    return render(request, 'review/review_form.html', {'product': product})

#모든 리뷰 가져오기
@login_required
def list_review(request):
    #모든 리뷰
    reviews = Review.objects.all().order_by('-created_at') 
    #리뷰 개수
    review_count = reviews.count()
    #착용한 상품 목록
    worn_products = WornProduct.objects.select_related('product').filter(user=request.user)
    # 착용한 상품 개수
    worn_product_count = worn_products.count()

    return render(request, 'review/review.html', {
        'reviews': reviews,
        'worn_product_count': worn_product_count,
        'products': [wp.product for wp in worn_products],
    })

#리뷰 상세
def detail_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, '', {'review': review}) #리뷰 상세 페이지로 이동 연결 해야함

#리뷰 수정
@login_required
def update_review(request, id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review.satisfaction = request.POST.get('satisfaction')
        review.size_feel = request.POST.get('size_feel')
        review.rating = request.POST.get('rating')
        review.title = request.POST.get('title')
        review.content = request.POST.get('content')
        review.save()
        return redirect('list_review')

    return render(request, 'review/review_form.html', {'review': review, 'is_update': True})

#리뷰 삭제
@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('list_review')

#리뷰 좋아요
@login_required
def likes(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)

    return redirect('product_review', product_id=review.product.id)