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
