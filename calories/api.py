import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Sum, Value, CharField, Avg, DateField, IntegerField, Count
from django.db.models.functions import Coalesce, Concat, Trunc, TruncMonth
from ninja import Router, UploadedFile, File, Form
from ninja.security import django_auth, HttpBearer
from ninja.errors import HttpError
from ninja.responses import codes_2xx, codes_4xx, codes_5xx

from accounts.api import CaloriesMadeAuth, Message, DateSchema, DictResponseSchema
from accounts.models import Token as AuthToken, Profile
from accounts.schema import RegisterFormSchema, LoginFormSchema
from calories.models import AteFoods, FoodBookMark, WorkoutSettings, WorkedOuts, WorkOutBookMark, Photo, WeightAndPhoto
from calories.schema import FoodSaveSchema, AteFoodsListsSchema, FoodUpdateSchema, FoodDeleteSchema, \
    FoodBookMarkSaveSchema, FoodBookMarkSaveSchemaList, FoodBookMarkPkSchema, WorkOutSystemListSchema, \
    WorkoutSaveSchema, WorkedoutListsSchema, WorkOutBookMarkSaveSchemaList, WorkOutBookMarkSaveSchema, \
    WorkOutBookMarkPkSchema, WeightSaveSchema, WeightPhotoSchemaList, ListResponse, DictResponse, \
    DashBoardResponseSchema

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
    sum_kcal = worked.aggregate(total=Coalesce(Sum('total_kcal'), 0.0))['total']  # total_kcal이 float 임

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


# TODO 운동즐겨찾기 목록
@router.post(
    '/workout/list/bookmark',
    auth=CaloriesMadeAuth(),
    summary="운동 즐겨찾기 목록",
    response={200: WorkOutBookMarkSaveSchemaList}
)
def workout_list_bookmark(request):
    user = User.objects.get(account_auth_token=request.auth)
    obj = WorkOutBookMark.objects.filter(user=user)

    return 200, {
        'workout_book_mark_list': list(obj)
    }


# TODO 운동즐겨찾기 등록
@router.post(
    '/workout/bookmark/save',
    auth=CaloriesMadeAuth(),
    summary="운동 즐겨찾기 등록",
    response={201: Message}
)
def workout_bookmark_save(request, data: WorkOutBookMarkSaveSchema):
    request_data = data.dict()
    user = User.objects.get(account_auth_token=request.auth)
    obj = WorkOutBookMark.objects.create(
        user=user,
        workout_name=request_data['workout_name'],
        mets=request_data['mets']
    )

    return 201, {
        "message": f"{obj.id}"
    }


# TODO 운동즐겨찾기 삭제
@router.post(
    '/workout/bookmark/delete',
    auth=CaloriesMadeAuth(),
    summary="운동 즐겨찾기 삭제",
    response={201: Message}
)
def workout_bookmark_delete(request, data: WorkOutBookMarkPkSchema):
    request_data = data.dict()
    print(request_data)
    WorkOutBookMark.objects.get(pk=request_data['id']).delete()

    return 201, {
        "message": 'success'
    }


# TODO 이미지만 저장(사용안함)
@router.post(
    '/photo/upload',
    auth=CaloriesMadeAuth(),
    summary="사진 사전업로드",
    response={201: Message}
)
# def weight_and_photo_save(request, weight: float, save_date: datetime.date, file: UploadedFile = File(...)):
def photo_upload(request, file: UploadedFile = File(...)):
# def photo_upload(request, file: file = Form(...)):
    print(request)
    print(file)
    user = User.objects.get(account_auth_token=request.auth)

    obj = Photo.objects.create(user=user, photo=file)
    print(obj.photo)
    print(obj.photo.url)
    # user = User.objects.get(account_auth_token=request.auth)
    # obj = WorkOutBookMark.objects.create(
    #     user=user,
    #     workout_name=request_data['workout_name'],
    #     mets=request_data['mets']
    # )
    make_full_url = request.build_absolute_uri(obj.photo.url)
    print(make_full_url)

    return 201, {
        "message": f"{make_full_url}"
    }


# TODO 체중 저장
@router.post(
    '/weight/save',
    auth=CaloriesMadeAuth(),
    summary="체중 및 사진 등록",
    response={201: Message}
)
# def weight_and_photo_save(request, weight: float, save_date: datetime.date, file: UploadedFile = File(...)):
def weight_and_photo_save(request, data: WeightSaveSchema, file: UploadedFile = File(...)):
    user = User.objects.get(account_auth_token=request.auth)
    request_data = data.dict()

    WeightAndPhoto.objects.create(
        user=user,
        weight=request_data['weight'],
        photo=file,
        photo_full_url=f'https://calorie-made-storage.s3.amazonaws.com/media/{file.name}',
        save_date=request_data['save_date']
    )
    profile = Profile.objects.get(user=user)
    profile.weight = request_data['weight']
    profile.save()

    return 201, {
        "message": "success"
    }


# TODO 눈바디 이미지 목록
@router.get(
    '/photo/list',
    auth=CaloriesMadeAuth(),
    summary="유져별 눈바디 사진 목록",
    response={200: WeightPhotoSchemaList}
)
def photos_list(request):
    user = User.objects.get(account_auth_token=request.auth)
    obj = WeightAndPhoto.objects.filter(user=user, photo__isnull=False).order_by('-save_date')

    result = {
        'photos': list(obj)
    }

    return 200, result


# TODO 일별기록
@router.get(
    '/graph/daily',
    auth=CaloriesMadeAuth(),
    summary="일별기록",
    response={200: DictResponse}
)
def daily_avg(request):
    before_seven_days = datetime.datetime.now()-datetime.timedelta(days=7)
    print('datetime.datetime.now()')
    print(datetime.datetime.now())
    print('before_seven_days')
    print(before_seven_days)

    user = User.objects.get(account_auth_token=request.auth)
    ates = AteFoods.objects.filter(
        user=user,
        ate_date__gte=datetime.datetime.now()-datetime.timedelta(days=7)
    ).values(
        'user',
        'ate_date'
    ).annotate(
        kcal=Coalesce(Sum('total_kcal'), 0)
    ).order_by('ate_date')

    worked = WorkedOuts.objects.filter(
        user=user,
        workedout_date__gte=datetime.datetime.now() - datetime.timedelta(days=7)
    ).values(
        'user',
        'workedout_date'
    ).annotate(
        kcal=Coalesce(Sum('total_kcal'), 0.0)
    ).order_by('workedout_date')

    weights = WeightAndPhoto.objects.filter(
        user=user,
        save_date__gte=datetime.datetime.now() - datetime.timedelta(days=7)
    ).values(
        'user',
        'save_date'
    ).annotate(
        avg_weight=Coalesce(Avg('weight'), 0.0),
    ).order_by('save_date')


    result = {
        'ate': list(ates),
        'worked': list(worked),
        'weight': list(weights)
    }
    return 200, {
        "message": result
    }


# TODO 월별기록
@router.get(
    '/graph/monthly',
    auth=CaloriesMadeAuth(),
    summary="월별기록",
    response={200: DictResponse}
)
def monthly_avg(request):
    user = User.objects.get(account_auth_token=request.auth)
    ates = AteFoods.objects.filter(
        user=user,
        ate_date__gte=datetime.datetime.now()-datetime.timedelta(days=365)
    ).annotate(month=TruncMonth('ate_date')).values(
        'user',
        'month'
    ).annotate(
        kcal=Coalesce(Sum('total_kcal'), 0)
    ).order_by('month')

    worked = WorkedOuts.objects.filter(
        user=user,
        workedout_date__gte=datetime.datetime.now() - datetime.timedelta(days=365)
    ).annotate(month=TruncMonth('workedout_date')).values(
        'user',
        'month'
    ).annotate(
        kcal=Coalesce(Sum('total_kcal'), 0.0),
    ).order_by('month')

    weights = WeightAndPhoto.objects.filter(
        user=user,
        save_date__gte=datetime.datetime.now() - datetime.timedelta(days=365)
    ).annotate(month=TruncMonth('save_date')).values(
        'user',
        'month'
    ).annotate(
        avg_weight=Coalesce(Avg('weight'), 0.0),
    ).order_by('month')

    result = {
        'ate': list(ates),
        'worked': list(worked),
        'weight': list(weights)
    }
    return 200, {
        "message": result
    }


# TODO 대시보드
@router.get(
    '/dashboard',
    auth=CaloriesMadeAuth(),
    summary="대시보드",
    response={200: DashBoardResponseSchema}
)
def dashboard(request):
    # datetime_start_ko = datetime.datetime.now().date()
    # datetime_start_ko = datetime_start_ko.strftime('%Y-%m-%d 00:00:00')
    # datetime_start_ko = datetime.datetime.strptime(datetime_start_ko, '%Y-%m-%d 00:00:00')
    today_hour = datetime.datetime.now().hour
    today_min = datetime.datetime.now().minute
    total_min_today = today_hour * 60 + today_min

    user = User.objects.get(account_auth_token=request.auth)
    ates = AteFoods.objects.filter(
        user=user,
        ate_date__gte=datetime.datetime.now() - datetime.timedelta(days=1)
    ).values(
        'user',
        'ate_date'
    ).annotate(
        kcal=Coalesce(Sum('total_kcal'), 0)
    ).order_by('ate_date')

    worked = WorkedOuts.objects.filter(
        user=user,
        workedout_date__gte=datetime.datetime.now() - datetime.timedelta(days=1)
    ).values(
        'user',
        'workedout_date'
    ).annotate(
        kcal=Coalesce(Sum('total_kcal'), 0.0),
        total_worked_min=Coalesce(Sum('many'), 0)
    ).order_by('workedout_date')
    user_info = Profile.objects.filter(user=user)[0]

    result = {
        "user_weight": user_info.weight,
        "user_target_weight": user_info.target_weight,
        "user_target_kcal": user_info.target_kcal,
        "total_min_today": total_min_today,
        "worked": list(worked),
        "ate": list(ates)
    }
    return 200, result
