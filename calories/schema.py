from ninja import Schema, ModelSchema
from datetime import date, datetime
from typing import List

from accounts.models import Profile
from calories.models import AteFoods, FoodBookMark, WorkoutSettings, WorkedOuts, WorkOutBookMark, WeightAndPhoto


class ListResponse(Schema):
    message: list


class DictResponse(Schema):
    message: dict


class UserInfo(Schema):
    class Config:
        model = Profile
        model_fields = "__all__"


class DashBoardResponseSchema(Schema):
    # user_info: dict
    # user_info: UserInfo
    user_weight: float = None
    user_target_weight: int = None
    user_target_kcal: int = None
    total_min_today: int = None
    worked: list = None
    ate: list = None


class FoodSaveSchema(Schema):
    key_string: str = None
    food_name: str = None
    base_kcal: float = None
    unit: float = None
    many: float = None
    total_unit_gram: float = None
    total_kcal: float = None
    ate_date: date = None


class FoodUpdateSchema(Schema):
    key_string: str = None
    many: float = None
    total_unit_gram: float = None
    total_kcal: float = None


class FoodDeleteSchema(Schema):
    key_string: str = None


class AteFoodsListModelSchema(ModelSchema):
    class Config:
        model = AteFoods
        model_fields = "__all__"
        # model_fields = ['id', 'category_name', 'order_num']


class AteFoodsListsSchema(Schema):
    totalKcalToday: float = None
    todayEatingList: List[AteFoodsListModelSchema] = None


class FoodBookMarkSaveSchema(Schema):
    food_name: str = None
    base_kcal: float = None
    unit: float = None


class FoodBookMarkModelSchema(ModelSchema):
    class Config:
        model = FoodBookMark
        model_fields = "__all__"


class FoodBookMarkPkSchema(Schema):
    id: int = None


class FoodBookMarkSaveSchemaList(Schema):
    food_book_mark_list: List[FoodBookMarkModelSchema] = None


class WorkOutSystemModelSchema(ModelSchema):
    class Config:
        model = WorkoutSettings
        model_fields = "__all__"


class WorkOutSystemListSchema(Schema):
    workout_system_list: List[WorkOutSystemModelSchema] = None

# workout_name = models.CharField(max_length=100)
# mets = models.FloatField()
# order_num = models.PositiveIntegerField(default=0)


class WorkoutSaveSchema(Schema):
    key_string: str = None
    workout_name: str = None
    mets: float = None
    base_kcal: float = None
    many: int = None
    total_kcal: float = None
    workedout_date: date = None
    workedout_start: datetime = None
    workedout_end: datetime = None


class WorkedoutListModelSchema(ModelSchema):
    class Config:
        model = WorkedOuts
        model_fields = "__all__"


class WorkedoutListsSchema(Schema):
    totalKcalToday: float = None
    todayWorkingoutList: List[WorkedoutListModelSchema] = None


# TODO 운동 즐겨찾기
class WorkOutBookMarkSaveSchema(Schema):
    workout_name: str = None
    mets: float = None


class WorkOutBookMarkModelSchema(ModelSchema):
    class Config:
        model = WorkOutBookMark
        model_fields = "__all__"


class WorkOutBookMarkPkSchema(Schema):
    id: int = None


class WorkOutBookMarkSaveSchemaList(Schema):
    workout_book_mark_list: List[WorkOutBookMarkModelSchema] = None


# user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='user_weight_and_photo')
# weight = models.PositiveIntegerField()  # 몸무게 kg
# photo = models.ImageField(null=True, blank=True)
# save_date = models.DateTimeField()  # 설정 저장 날짜

# TODO 체중 및 사진 저장
class WeightSaveSchema(Schema):
    weight: float
    # photo: float = None
    save_date: date


class WeightModelSchema(ModelSchema):
    full_url: str = None

    class Config:
        model = WeightAndPhoto
        model_fields = ['id', 'weight', 'photo', 'save_date', 'photo_full_url']


class WeightWithFullURLSchema(Schema):
    weight: float
    photo: str
    save_date: date


# class WorkOutBookMarkPkSchema(Schema):
#     id: int = None


class WeightPhotoSchemaList(Schema):
    photos: List[WeightModelSchema] = None
