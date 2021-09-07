from django.conf import settings
from django.db import models


class Profile(models.Model):  # 1:1
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    sex = models.PositiveSmallIntegerField(blank=True, null=True)  # 1이면 남자, 2이면 여자 3이면 중성
    birth = models.DateField(null=True, blank=True)  # 생일
    height = models.PositiveIntegerField(blank=True, null=True)  # 키 cm
    weight = models.PositiveIntegerField(blank=True, null=True)  # 몸무게 kg

    def __str__(self):
        return self.user.username
