from django.db import models

# userprofile/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bust = models.IntegerField(null=True, blank=True)         # 윗가슴
    underbust = models.IntegerField(null=True, blank=True)    # 밑가슴
    pelvis_size = models.CharField(max_length=10, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}의 프로필"

