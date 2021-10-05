from django.conf import settings
from django.db import models

from accounts.models import Profile


class FitnessSpec(models.Model):  # 운동종류들 저장하는 테이블
    spec = models.CharField(max_length=100, default='운동이름')
    icon = models.CharField(max_length=255, blank=True, null=True)  # 운동 이미지
    calorie = models.PositiveIntegerField()  # 소모칼로리 / 1분

    def __str__(self):
        return self.spec


class FitnessActivate(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fitness = models.ForeignKey(FitnessSpec, on_delete=models.SET_NULL, null=True, blank=True) # 달리기, 1 primarykey
    minute = models.PositiveIntegerField(default=0)
    consumed_calories = models.PositiveIntegerField(default=0)
    worked_at = models.DateTimeField(auto_now_add=True)  # default=timezone.now()

    def __str__(self):
        return f"{self.user.user.username}가 {self.fitness}을 {self.minute}동안 {self.worked_at}에 했음."

    def user_consumed_calories(self):
        user_weight = self.user.weight
        # 칼로리 계산법
        # 운동 칼로리 X 몸무게 X 분
        consumed = user_weight * self.fitness.calorie * self.minute
        return consumed


class FoodSpec(models.Model):  # 음식종류들 저장하는 테이블
    spec = models.CharField(max_length=100, default='음식이름')
    icon = models.CharField(max_length=255, blank=True, null=True)  # 음식 이미지
    calorie = models.PositiveIntegerField()  # 섭취칼로리 / 1회제공량

    def __str__(self):
        return self.spec


class IncomeFoods(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodSpec, on_delete=models.SET_NULL, null=True, blank=True)
    portion = models.PositiveIntegerField(default=0)
    income_calories = models.PositiveIntegerField(default=0)
    income_at = models.DateTimeField(auto_now_add=True)  # default=timezone.now()

    def __str__(self):
        return f"{self.user.user.username}가 {self.food}을 {self.portion}만큼 {self.income_at}에 섭취했음."
