from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models.functions import Coalesce
from ninja import Router, Form, Schema
from ninja.security import django_auth, HttpBearer
from ninja.errors import HttpError
from ninja.responses import codes_2xx, codes_4xx, codes_5xx

from accounts.api import CaloriesMadeAuth, Message, DateSchema, DictResponseSchema
from accounts.models import Token as AuthToken, Profile
from accounts.schema import RegisterFormSchema, LoginFormSchema
from calories.models import AteFoods, FoodBookMark, WorkoutSettings, WorkedOuts
from calories.schema import FoodSaveSchema, AteFoodsListsSchema, FoodUpdateSchema, FoodDeleteSchema, \
    FoodBookMarkSaveSchema, FoodBookMarkSaveSchemaList, FoodBookMarkPkSchema, WorkOutSystemListSchema, \
    WorkoutSaveSchema, WorkedoutListsSchema

router = Router()


# TODO 식단저장
@router.post(
    '/food/save',
    auth=CaloriesMadeAuth(),
    summary="식사기록 저장",
    response={201: Message}
)
def food_save(request, data: FoodSaveSchema):
    request_data = data.dict()
    token = AuthToken.objects.get(key=request.auth)  # 토큰 만료처리 해야할수도 있음
    user = User.objects.get(pk=token.user.pk)
    AteFoods.objects.create(
        user=user,
        key_string=request_data['key_string'],
        food_name=request_data['food_name'],
        base_kcal=request_data['base_kcal'],
        unit=request_data['unit'],
        many=request_data['many'],
        total_unit_gram=request_data['total_unit_gram'],
        total_kcal=request_data['total_kcal'],
        ate_date=request_data['ate_date']
    )

    return 201, {
        "message": 'success'
    }


# TODO 식단업데이트
@router.put(
    '/food/update',
    auth=CaloriesMadeAuth(),
    summary="식사기록 수정",
    response={201: Message, 404: Message, 500: Message}
)
def food_update(request, data: FoodUpdateSchema):
    request_data = data.dict()
    token = AuthToken.objects.get(key=request.auth)  # 토큰 만료처리 해야할수도 있음
    user = User.objects.get(pk=token.user.pk)

    try:
        obj = AteFoods.objects.get(user=user, key_string=request_data['key_string'])
        obj.many = request_data['many']
        obj.total_unit_gram = request_data['total_unit_gram']
        obj.total_kcal = request_data['total_kcal']
        obj.save()

        return 201, {
            "message": 'success'
        }
    except AteFoods.DoesNotExist as ade:
        print(f'error 404 : {ade}')
        return 404, {
            "message": f"오브젝트를 찾을 수 없습니다. 앱을 다시 시작 해 주십시요. Code[404] : {ade}"
        }

    except Exception as e:
        return 500, {
            f"message : 서버에러. Code[500] : {e}"
        }


# TODO 식단삭제
@router.put(
    '/food/delete',
    auth=CaloriesMadeAuth(),
    summary="식사기록 삭제",
    response={201: Message, 404: Message, 500: Message}
)
def food_delete(request, data: FoodDeleteSchema):
    request_data = data.dict()
    token = AuthToken.objects.get(key=request.auth)  # 토큰 만료처리 해야할수도 있음
    user = User.objects.get(pk=token.user.pk)

    try:
        obj = AteFoods.objects.get(user=user, key_string=request_data['key_string'])
        obj.delete()

        return 201, {
            "message": 'success'
        }
    except AteFoods.DoesNotExist as ade:
        print(f'error 404 : {ade}')
        return 404, {
            "message": f"오브젝트를 찾을 수 없습니다. 앱을 다시 시작 해 주십시요. Code[404] : {ade}"
        }

    except Exception as e:
        return 500, {
            f"message : 서버에러. Code[500] : {e}"
        }


# TODO 그날 먹은 음식 목록
@router.post(
    '/food/list/day',
    auth=CaloriesMadeAuth(),
    summary="그날 먹은 음식들",
    response={200: AteFoodsListsSchema}
)
def food_list_day(request, data: DateSchema):
    request_data = data.dict()
    user = User.objects.get(account_auth_token=request.auth)
    ate = AteFoods.objects.filter(user=user, ate_date=request_data['date'])
    sum_kcal = ate.aggregate(total=Coalesce(Sum('total_kcal'), 0))['total']

    return 200, {
        # 'totalKcalToday': sum_kcal['total_kcal__sum'],
        'totalKcalToday': sum_kcal,
        'todayEatingList': list(ate)
    }


# TODO 음식즐겨찾기 목록
@router.post(
    '/food/list/bookmark',
    auth=CaloriesMadeAuth(),
    summary="음식 즐겨찾기 목록",
    response={200: FoodBookMarkSaveSchemaList}
)
def food_list_bookmark(request):
    user = User.objects.get(account_auth_token=request.auth)
    ate = FoodBookMark.objects.filter(user=user)

    return 200, {
        # 'totalKcalToday': sum_kcal['total_kcal__sum'],
        'food_book_mark_list': list(ate)
    }


# TODO 음식즐겨찾기 등록
@router.post(
    '/food/bookmark/save',
    auth=CaloriesMadeAuth(),
    summary="음식 즐겨찾기 등록",
    response={201: Message}
)
def food_bookmark_save(request, data: FoodBookMarkSaveSchema):
    request_data = data.dict()
    user = User.objects.get(account_auth_token=request.auth)
    FoodBookMark.objects.create(
        user=user,
        food_name=request_data['food_name'],
        base_kcal=request_data['base_kcal'],
        unit=request_data['unit']
    )

    return 201, {
        "message": 'success'
    }


# TODO 음식즐겨찾기 삭제
@router.post(
    '/food/bookmark/delete',
    auth=CaloriesMadeAuth(),
    summary="음식 즐겨찾기 삭제",
    response={201: Message}
)
def food_bookmark_delete(request, data: FoodBookMarkPkSchema):
    request_data = data.dict()
    FoodBookMark.objects.get(pk=request_data['id']).delete()

    return 201, {
        "message": 'success'
    }


# eating = {
#   totalKcalToday: 630,
#   todayEatingList: [
#     {
#       keyString: 'sdag32df',
#       which: {what: '밥', baseKcal: 150, unit: '100'},
#       many: 2,
#       totalUnits: 200,
#       thisTotal: 300,
#     },
#     {
#       keyString: '11nKRGee',
#       which: {what: '사과', baseKcal: 35, unit: '100'},
#       many: 1,
#       totalUnits: 100,
#       thisTotal: 35,
#     },
#     {
#       keyString: '8hjiweP',
#       which: {what: '홈런볼', baseKcal: 150, unit: '80'},
#       many: 1,
#       totalUnits: 80,
#       thisTotal: 150,
#     },
#     {
#       keyString: '926HHGErd',
#       which: {what: '매일두유', baseKcal: 115, unit: '120'},
#       many: 3,
#       totalUnits: 120,
#       thisTotal: 145,
#     },
#   ],
# }


# TODO 운동목록
@router.get(
    '/workout/list/system',
    auth=CaloriesMadeAuth(),
    summary="시스템 운동목록",
    response={200: WorkOutSystemListSchema}
)
def workout_system_list(request, workout_name: str = None):
    if workout_name:
        print('got workout_name is ', workout_name)
        obj = WorkoutSettings.objects.filter(workout_name__contains=workout_name)

    else:
        print('got workout_name is ', workout_name)
        obj = WorkoutSettings.objects.all()

    result = {
        'workout_system_list': list(obj)
    }

    return 200, result


# TODO 운동저장
@router.post(
    '/workout/save',
    auth=CaloriesMadeAuth(),
    summary="식사기록 저장",
    response={201: Message}
)
def workedout_save(request, data: WorkoutSaveSchema):
    request_data = data.dict()
    user = User.objects.get(account_auth_token=request.auth)
    WorkedOuts.objects.create(
        user=user,
        key_string=request_data['key_string'],
        workout_name=request_data['workout_name'],
        mets=request_data['mets'],
        base_kcal=request_data['base_kcal'],
        many=request_data['many'],
        total_kcal=request_data['total_kcal'],
        workedout_date=request_data['workedout_date'],
        workedout_start=request_data['workedout_start'],
        workedout_end=request_data['workedout_end'],
    )

    return 201, {
        "message": 'success'
    }


# TODO 그날 한 운동 목록
@router.post(
    '/workout/list/day',
    auth=CaloriesMadeAuth(),
    summary="그날 한 운동들",
    response={200: WorkedoutListsSchema}
)
def workedout_list_day(request, data: DateSchema):
    request_data = data.dict()
    user = User.objects.get(account_auth_token=request.auth)
    worked = WorkedOuts.objects.filter(user=user, workedout_date=request_data['date'])
    sum_kcal = worked.aggregate(total=Coalesce(Sum('total_kcal'), 0))['total']

    return 200, {
        # 'totalKcalToday': sum_kcal['total_kcal__sum'],
        'totalKcalToday': sum_kcal,
        'todayWorkingoutList': list(worked)
    }


# TODO 운동업데이트
@router.put(
    '/workout/update',
    auth=CaloriesMadeAuth(),
    summary="운동기록 수정",
    response={201: Message, 404: Message, 500: Message}
)
def worked_update(request, data: FoodUpdateSchema):
    request_data = data.dict()
    user = User.objects.get(account_auth_token=request.auth)

    try:
        obj = WorkedOuts.objects.get(user=user, key_string=request_data['key_string'])
        obj.many = request_data['many']
        obj.total_kcal = request_data['total_kcal']
        obj.save()

        return 201, {
            "message": 'success'
        }
    except AteFoods.DoesNotExist as ade:
        print(f'error 404 : {ade}')
        return 404, {
            "message": f"오브젝트를 찾을 수 없습니다. 앱을 다시 시작 해 주십시요. Code[404] : {ade}"
        }

    except Exception as e:
        return 500, {
            f"message : 서버에러. Code[500] : {e}"
        }


# TODO 운동삭제
@router.put(
    '/workout/delete',
    auth=CaloriesMadeAuth(),
    summary="운동기록 삭제",
    response={201: Message, 404: Message, 500: Message}
)
def worked_delete(request, data: FoodDeleteSchema):
    request_data = data.dict()
    user = User.objects.get(account_auth_token=request.auth)

    try:
        obj = WorkedOuts.objects.get(user=user, key_string=request_data['key_string'])
        obj.delete()

        return 201, {
            "message": "success"
        }

    # class Message(Schema):
    #     message: str
    except AteFoods.DoesNotExist as ade:
        print(f'error 404 : {ade}')
        return 404, {
            "message": f"오브젝트를 찾을 수 없습니다. 앱을 다시 시작 해 주십시요. Code[404] : {ade}"
        }

    except Exception as e:
        return 500, {
            f"message : 서버에러. Code[500] : {e}"
        }