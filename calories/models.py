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
    unit = models.PositiveIntegerField(blank=True, null=True)  # 1회 제공량 g


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


# {
#   keyString: '11nKRGee',
#   which: {what: '사과', baseKcal: 35, unit: '100'},
#   many: 1,
#   totalUnits: 100,
#   thisTotal: 35,
# },

class AteFoods(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='user_ate_food')
    key_string = models.CharField(max_length=100)  # unique key string
    food_name = models.CharField(max_length=100)  # 음식이름
    base_kcal = models.PositiveIntegerField()  # 1회제공량당 칼로리
    unit = models.PositiveIntegerField()  # 1회제공량 그램
    many = models.PositiveIntegerField()  # 1회제공량 기준 몇개(0.5, 1, 1.5, 2 ...)
    total_unit_gram = models.PositiveIntegerField()  # 총 섭취 그램수
    total_kcal = models.PositiveIntegerField()  # 총 섭취 칼로리
    ate_date = models.DateField()  # 섭취 일자
    created_at = models.DateTimeField(auto_now_add=True)


class FoodBookMark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='user_food_bookmark')
    food_name = models.CharField(max_length=100)  # 음식이름
    base_kcal = models.PositiveIntegerField()  # 1회제공량당 칼로리
    unit = models.PositiveIntegerField()  # 1회제공량 그램
    created_at = models.DateTimeField(auto_now_add=True)


class WorkoutSettings(models.Model):
    workout_name = models.CharField(max_length=100)
    mets = models.FloatField()
    order_num = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order_num']


class WorkedOuts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='user_worked_out')
    key_string = models.CharField(max_length=100)  # unique key string
    workout_name = models.CharField(max_length=100)  # 음식이름
    mets = models.FloatField()  # met / 1분
    base_kcal = models.FloatField()  # met * 몸무게 * 3.5 * 분 / 200
    many = models.PositiveIntegerField()  # 몇분
    total_kcal = models.FloatField()  # 총 소모 칼로리 (칼로리 * 분)
    workedout_date = models.DateField()  # 운동 일자
    workedout_start = models.DateTimeField(null=True, blank=True)  # 운동시작
    workedout_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WorkOutBookMark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='user_workout_bookmark')
    workout_name = models.CharField(max_length=100)  # 운동이름
    # base_kcal = models.PositiveIntegerField()
    mets = models.PositiveIntegerField()  # met / 1분
    created_at = models.DateTimeField(auto_now_add=True)
