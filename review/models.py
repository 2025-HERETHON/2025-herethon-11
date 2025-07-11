from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
class Review(models.Model):
    SATISFACTION_CHOICES = [
        ('good', '만족해요'),
        ('soso', '보통이에요'),
        ('bad', '별로예요'),
    ]

    SIZE_FEEL_CHOICES = [
        ('big', '크게 느껴져요'),
        ('normal', '적당해요'),
        ('small', '작게 느껴져요'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews') #리뷰 작성자
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #리뷰 대상 상품
    satisfaction = models.CharField(max_length=10, choices=SATISFACTION_CHOICES) #만족도
    size_feel = models.CharField(max_length=10, choices=SIZE_FEEL_CHOICES) #사이즈
    rating = models.PositiveSmallIntegerField()  # 별점 1~5
    title = models.CharField(max_length=30) #제목
    content = models.TextField(max_length=300, blank=True) #내용
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(User, related_name='liked_reviews', blank=True)

    def __str__(self):
        return f"[{self.product}] {self.user.username} - {self.title}"