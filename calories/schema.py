from ninja import Schema, ModelSchema
from datetime import date
from typing import List


from calories.models import AteFoods, FoodBookMark


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


# user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
#     food_name = models.CharField(max_length=100)  # 음식이름
#     base_kcal = models.PositiveIntegerField()  # 1회제공량당 칼로리
#     unit = models.PositiveIntegerField()  # 1회제공량 그램


# class FoodBookMark