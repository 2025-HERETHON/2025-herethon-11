from django.db import models

# userprofile/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #사용자 정보
    nickname = models.CharField(max_length=10, unique=True, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    #체형 정보
    bust = models.IntegerField(null=True, blank=True)         # 윗가슴
    underbust = models.IntegerField(null=True, blank=True)    # 밑가슴
    cup_size = models.CharField(max_length=15, null=True, blank=True) #가슴 사이즈
    waist = models.IntegerField(null=True, blank=True) #허리 둘레
    hip = models.IntegerField(null=True, blank=True) #힙 둘레
    pelvis_size = models.CharField(max_length=10, null=True, blank=True) #골반 둘레
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    #수동 입력 여부
    is_manual_cup = models.BooleanField(default=False) #false: 자동입력/ true: 직접입력
    is_manual_pelvis = models.BooleanField(default=False)

    #체형 공개 여부
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}의 프로필"

