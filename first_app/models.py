from django.db import models
from django.conf import settings


class House(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 1대N
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # 1대N
    address = models.CharField(max_length=100)
    tel = models.IntegerField(blank=True)
    post_num = models.IntegerField(blank=True)


class Board(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 1대N
    title = models.CharField(max_length=100)  # 글제목
    content = models.TextField()  # 글내용
    created_at = models.DateTimeField(auto_now_add=True)  # 자동으로 날짜 저장 글저장시
    updated_at = models.DateTimeField(auto_now=True)  # 글 수정 날짜
    hidden = models.BooleanField(default=False)  # True or False

    def __str__(self):
        return self.title


