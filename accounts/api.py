from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ninja import Router, Form, Schema
from ninja.security import django_auth, HttpBearer
from ninja.errors import HttpError
from ninja.responses import codes_2xx, codes_4xx, codes_5xx

from accounts.models import Token as AuthToken, Profile
from accounts.schema import RegisterFormSchema, LoginFormSchema, OnlyMessageResponseSchema, TargetWeightChangeSchema, \
    TargetChangeSchema, OnlyStringRequestSchema, OnlyListMessageResponseSchema
from datetime import date

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


class CaloriesMadeAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            token = AuthToken.objects.get(key=token)
            user = User.objects.get(pk=token.user.pk)

            return token.key
        except AuthToken.DoesNotExist as ad:
            print(f'{token}. does not exists, auth failed : {ad}')
            return None
        except Exception as e:
            print(f'token : {token} for authentication server error : {e}')


class Token(Schema):
    token: str
    username: str
    # expires: date


class UserInfo(Schema):
    token: str
    user_id: int
    username: str
    sex: int
    birth: str = None
    height: float
    weight: float
    nickname: str
    target_kcal: int
    target_weight: int


class Message(Schema):
    message: str


class DateSchema(Schema):
    date: date


class DictResponseSchema(Schema):
    resp: dict


@router.post("/login", auth=None, response={200: UserInfo, 401: Message, 403: Message}, tags=['Auth'])  # < overriding global auth
def login(request, data: LoginFormSchema):
    try:
        request_data = data.dict()
        username = request_data['username']
        password = request_data['password']
        user = authenticate(request, username=username, password=password)  # username과 password가 DB에 있는지 없으면 None반환
        if user is not None:
            # user가 none이 아니면 토큰 생성 또는 업데이트
            obj, created = AuthToken.objects.update_or_create(user=user)

            user_id = user.id
            user_sex = user.user_profile.sex
            user_birth = user.user_profile.birth
            user_height = user.user_profile.height
            user_weight = user.user_profile.weight
            user_nickname = user.user_profile.nickname
            target_kcal = user.user_profile.target_kcal
            target_weight = user.user_profile.target_weight

            return {
                "token": obj.key,
                "user_id": user_id,
                'username': username,
                "sex": user_sex,
                "birth": user_birth,
                "height": user_height,
                "weight": user_weight,
                "nickname": user_nickname,
                "target_kcal": target_kcal,
                "target_weight": target_weight,
            }
        else:
            return 401, {'message': f'이메일 또는 비밀번호를 확인 해 주세요.'}
    except Exception as e:
        print('exception')
        return 403, {'message': f'이메일 또는 비밀번호를 확인 해 주세요 => {e}'}


@router.post("/register", auth=None, summary="회원가입", response={201: Token, 409: Message, 401: Message, 500: Message}, tags=['Auth'])
def register(
        request,
        data: RegisterFormSchema
        ):
    try:
        request_data = data.dict()
        username = request_data['username']
        password1 = request_data['password1']
        password2 = request_data['password2']
        sex = request_data['sex']
        birthday = request_data['birthday']
        weight = request_data['weight']
        height = request_data['height']
        nickname = request_data['nickname']
        target_kcal = request_data['target_kcal']
        target_weight = request_data['target_weight']

        user = authenticate(request, username=username, password=password1)  # username과 password가 DB에 있는지 없으면 None반환
        if user is not None:
            return 409, {'message': '이미 가입되어있는 이메일 주소 입니다.'}
        else:
            try:
                print('tring')
                validate_password(password1)
                validate_email(username)
                if password1 == password2:
                    print('2')
                    user = User.objects.create_user(username=username, email=username, password=password1)
                    user.save()
                    print('3')
                    created = AuthToken.objects.create(user=user)
                    created.save()
                    print('4')
                    Profile.objects.create(
                        user=user,
                        sex=sex,
                        birth=birthday,
                        height=height,
                        weight=weight,
                        nickname=nickname,
                        target_kcal=target_kcal,
                        target_weight=target_weight
                    )
                    print('5')
                    return 201, {"token": created.key, 'username': username}
                else:
                    return 401, {'message': '비밀번호가 서로 다릅니다.'}

            except ValidationError as ve:
                return 401, {'message': f'{ve}'}

    except Exception as e:
        print('exception')
        print('500 error : ', e)
        return 500, {'message': f'복합적인 에러 => {e}'}


# TODO 유져정보
@router.get(
    '/user/info',
    auth=CaloriesMadeAuth(),
    summary="유져기본정보",
    response={200: UserInfo}
)
def user_info(request):
    token = AuthToken.objects.get(key=request.auth)
    user = User.objects.get(pk=token.user.pk)
    return 200, {
        "token": request.auth,
        "user_id": user.id,
        'username': user.username,
        "sex": user.user_profile.sex,
        "birth": user.user_profile.birth,
        "height": user.user_profile.height,
        "weight": user.user_profile.weight,
        "nickname": user.user_profile.nickname,
        "target_kcal": user.user_profile.target_kcal,
        "target_weight": user.user_profile.target_weight,
    }


# TODO 유져목표체중&칼로리&키 변경
@router.put(
    '/user/info/target',
    auth=CaloriesMadeAuth(),
    summary="유져목표체중 변경",
    response={201: OnlyMessageResponseSchema}
)
def user_target_put(request, data: TargetChangeSchema):
    user = User.objects.get(account_auth_token=request.auth)
    data = data.dict()
    what = data['what']
    obj = Profile.objects.get(user=user)
    if what == 'weight':
        obj.target_weight = data['target']
    elif what == 'height':
        obj.height = data['target']
    elif what == 'kcal':
        obj.target_kcal = data['target']
    obj.save()

    return 201, {'message': 'ok'}


# TODO 이메일 유효성 검사
@router.post(
    '/validation/email',
    auth=None,
    summary="이메일유효성검사",
    response={200: OnlyMessageResponseSchema, 409: OnlyMessageResponseSchema, 500: OnlyMessageResponseSchema}
)
def email_validation(request, data: OnlyStringRequestSchema):
    request_data = data.dict()

    email = request_data['request_data']

    # validate_password(password1)

    try:
        validate_email(email)
        return 200, {
            "message": 'success'
        }
    except ValidationError as ve:
        return 409, {
            "message": f'{ve.message}'
        }
    except Exception as e:
        return 500, {
            "message": f'{e}'
        }


# TODO 비밀번호 유효성 검사
@router.post(
    '/validation/password',
    auth=None,
    summary="비밀번호유효성검사",
    response={200: OnlyMessageResponseSchema, 409: OnlyListMessageResponseSchema, 500: OnlyMessageResponseSchema}
)
def password_validation(request, data: OnlyStringRequestSchema):
    request_data = data.dict()
    password = request_data['request_data']

    try:
        validate_password(password)
        return 200, {
            "message": 'success'
        }
    except ValidationError as ve:

        return 409, {
            "message": ve.messages
        }
    except Exception as e:
        return 500, {
            "message": f'{e}'
        }