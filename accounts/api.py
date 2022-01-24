from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ninja import Router, Form, Schema
from ninja.security import django_auth, HttpBearer
from ninja.errors import HttpError
from ninja.responses import codes_2xx, codes_4xx, codes_5xx

from accounts.models import Token as AuthToken

router = Router()


# class AuthBearer(HttpBearer):
#     def authenticate(self, request, token):
#         if token == "supersecret":
#             return token


@router.get("/pets")
def pets(request):
    return f'Authenticated user {request.auth}'


@router.get("/bearer")
def bearer(request):
    return {"token": request.auth}


class Token(Schema):
    token: str
    username: str
    # expires: date


class Message(Schema):
    message: str



@router.post("/login", auth=None, response={200: Token, codes_4xx: Message})  # < overriding global auth
def login(request, username: str = Form(...), password: str = Form(...)):
    try:
        user = authenticate(request, username=username, password=password)  # username과 password가 DB에 있는지 없으면 None반환
        if user is not None:
            # user가 none이 아니면 토큰 생성 또는 업데이트
            obj, created = AuthToken.objects.update_or_create(user=user)

            return {"token": obj.key, 'username': username}
        else:
            return 401, {'message': f'이메일 또는 비밀번호를 확인 해 주세요.'}
    except Exception as e:
        print('exception')
        return 403, {'message': f'이메일 또는 비밀번호를 확인 해 주세요 => {e}'}


@router.post("/register", auth=None, response={201: Token, codes_4xx: Message, codes_5xx: Message})
def register(request, username: str = Form(...), password1: str = Form(...), password2: str = Form(...)):
    print(1 == 3)
    try:
        user = authenticate(request, username=username, password=password1)  # username과 password가 DB에 있는지 없으면 None반환
        if user is not None:
            return 409, {'message': '이미 가입되어있는 이메일 주소 입니다.'}
        else:
            try:
                validate_password(password1)
                validate_email(username)
                if password1 == password2:
                    user = User.objects.create_user(username=username, email=username, password=password1)
                    user.save()
                    created = AuthToken.objects.create(user=user)
                    created.save()
                    return 201, {"token": created.key, 'username': username}
                else:
                    return 401, {'message': '비밀번호가 서로 다릅니다.'}

            except ValidationError as ve:
                return 401, {'message': f'{ve}'}

    except Exception as e:
        print('exception')
        return 500, {'message': f'복합적인 에러 => {e}'}
