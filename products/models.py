from django.db import models
from django.contrib.auth.models import User


# subcategory DB
class SubCategory(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name


# 카테고리 (브래지어, 팬티, 패치)
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# 기본 상품 DB
class Product(models.Model):
    # 외부 고유 ID
    external_id = models.CharField(max_length = 100, unique = True)

    # 검색 키워드
    source_keyword = models.CharField(max_length=50, null=True, blank=True)

    # 상품명, 가격, 이미지 url, 상품 링크, 상점 이름
    title = models.CharField(max_length = 255)
    price = models.IntegerField()
    thumbnail_url = models.URLField()
    link = models.URLField()
    shop = models.CharField(max_length = 100, null = True, blank = True)

    # 카테고리 및 서브 카테고리
    categories = models.ManyToManyField(Category, blank=True)        # 예: 브래지어, 팬티, 패치
    subcategories = models.ManyToManyField(SubCategory, blank = True)  # 예: 스포츠 브라, 브라탑, 후크 등

    # 사이즈, 색상, 소재
    size = models.CharField(max_length = 50, blank = True, null = True)
    color = models.CharField(max_length = 50, blank = True, null = True)
    material = models.CharField(max_length = 50, blank = True, null = True)

    # 중간 테이블 없이 바로 유저 연결
    liked_users = models.ManyToManyField(User, related_name = 'liked_products', blank = True)

    # 등록된 시각
    created_at = models.DateTimeField(auto_now_add = True)

    # 상품명, 카테고리, 서브 카테고리 출력
    def __str__(self):
        subcats = ', '.join([sub.name for sub in self.subcategories.all()])
        cats = ', '.join([cat.name for cat in self.categories.all()])
        return f"{self.title} (Category: {cats} / Subcategories: {subcats})"


# 착용했던 상품 DB
class WornProduct(models.Model):
    # 착용한 유저, 상품 fk
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worn_products')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    # 착용했던 상품 DB 등록 시각
    created_at = models.DateTimeField(auto_now_add = True)

    # 착용했던 사이즈 및 색상
    size = models.CharField(max_length = 50, blank = True, null = True)
    color = models.CharField(max_length = 50, blank = True, null = True)

    # 유저 이름, 상품명, DB에 추가한 시각 출력
    def __str__(self):
        return f"{self.user.username} wore {self.product.title} at {self.created_at}"


class RecentlyViewedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')  # 같은 상품 중복 저장 방지
        ordering = ['-viewed_at']  # 최근 본 순서로 정렬


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.product.title} 이미지"