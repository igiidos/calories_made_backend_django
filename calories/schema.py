from ninja import Schema, ModelSchema
from datetime import date, datetime
from typing import List


from calories.models import AteFoods, FoodBookMark, WorkoutSettings, WorkedOuts


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
