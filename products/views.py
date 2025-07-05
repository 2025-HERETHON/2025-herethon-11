from django.shortcuts import render

# Create your views here.
# 추천 상품 반환
def recommand(request):
    return render(request, 'products/recommand.html')