from typing import List
from ninja import Schema, ModelSchema, Field


class RegisterFormSchema(Schema):
    username: str
    password1: str = None
    password2: str = None
    sex: int = None
    birthday: str = None
    nickname: str = None
    height: float = None
    weight: float = None
    target_kcal: int = None
    target_weight: int = None


class LoginFormSchema(Schema):
    username: str
    password: str


class TargetChangeSchema(Schema):
    what: str = None
    target: int = None


class TargetWeightChangeSchema(Schema):
    target: int = None


class TargetKcalChangeSchema(Schema):
    target: int = None


class HeightChangeSchema(Schema):
    target: int = None


class OnlyStringRequestSchema(Schema):
    request_data: str


class OnlyMessageResponseSchema(Schema):
    message: str = None


class OnlyListMessageResponseSchema(Schema):
    message: list
