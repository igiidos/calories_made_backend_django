from ninja import Schema, ModelSchema
from datetime import date
from typing import List


from calories.models import AteFoods


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

