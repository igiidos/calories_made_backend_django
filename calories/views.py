import datetime
from random import random, randrange

import requests
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from accounts.models import Profile
from calories.models import FitnessSpec, FitnessActivate, FoodSpec, IncomeFoods


def search_food(request):  # django argument request:
    # 이게 정보가 부족해서 아래와 같은 서비스를 사용 할 예정
    # https://platform.fatsecret.com/
    # igiidos 2717igii
    # OAuth2.0 정보
    # ClientID : 504ac2ac25b644f493b9c67bcf146d45
    # Client Secret : c88056cd25b643e9be388412374a5643
    # OAuth1.0 정보
    # Consumer key : 504ac2ac25b644f493b9c67bcf146d45
    # Consumer Secret : 6321b25a92d0483287dc6d2eed224c02

    # url = 'http://apis.data.go.kr/1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList'
    # params = {'serviceKey': 'BsfQgS+zkc2qI2dw8Aiyx/F106HRcpOi8SpPkMOJ1wT3jp1cGZnKSI7BIB6zzY48ciAI3ieVx2Ctq3qz+8ltdg==', 'desc_kor': '바나나칩', 'pageNo': '1', 'numOfRows': '3', 'bgn_year': '2017',
    #           'animal_plant': '(유)돌코리아', 'type': 'xml'}
    #
    # response = requests.get(url, params=params)
    # print(response.content)


    get_food = request.GET.get('food', None)
    print(get_food)

    # if get_food:
    #     food_name = get_food
    # else:
    #     food_name = '바나나칩'

    #https://apis.data.go.kr/1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList1?
    # serviceKey=BsfQgS%2Bzkc2qI2dw8Aiyx%2FF106HRcpOi8SpPkMOJ1wT3jp1cGZnKSI7BIB6zzY48ciAI3ieVx2Ctq3qz%2B8ltdg%3D%3D
    # &desc_kor=%EB%B0%94%EB%82%98%EB%82%98%EC%B9%A9
    # &pageNo=1
    # &numOfRows=3
    # &bgn_year=2017
    # &animal_plant=(%EC%9C%A0)%EB%8F%8C%EC%BD%94%EB%A6%AC%EC%95%84
    # &type=xml

    url = 'https://apis.data.go.kr/1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList1'
    params = {
        'serviceKey': 'BsfQgS+zkc2qI2dw8Aiyx/F106HRcpOi8SpPkMOJ1wT3jp1cGZnKSI7BIB6zzY48ciAI3ieVx2Ctq3qz+8ltdg==',
        # 'numOfRows': 3, # max 100
        # 'pageNo': 1,
        'type': 'json',
        # 'desc_kor': '사과',
        # 'bgn_year': 2017,
        # 'animal_plant': '(유)돌코리아'
        'desc_kor': get_food
    }

    food_list = requests.get(url, params=params, verify=False)

    if food_list.status_code != 200:
        foods = None

    else:
        food = food_list.json()
        print(food)

        try:
            if food['body']['totalCount']:
                foods = food['body']['items']
                for i in foods:
                    food_name = i['DESC_KOR']
                    person = i['SERVING_WT']
                    cal = i['NUTR_CONT1']
                    company = i['ANIMAL_PLANT']

                    print(f"{food_name} / {person}g / {cal}kcal / {company}")


            else:
                foods = None
        except Exception as e:
            foods = None

    context = {
        'foods': foods
    }

    return render(request, 'calories/food_lists.html', context)


@login_required
def calories_index(request):

    # count = 0
    # for i in range(20):
    #     spec = f'음식-{count}'  # 운동-0, 운동-1
    #     count += 1
    #     cal = randrange(1, 20)
    #
    #     obj = FoodSpec.objects.create(
    #         spec=spec,
    #         calorie=cal
    #     )
    #     obj.save()

    fitness = FitnessSpec.objects.all()
    foods = FoodSpec.objects.all()

    # 오늘 저장된 운동들의 칼로리 합계
    # 합계 데이터베이스 쿼리중에서 SUM, Minus, Avg => aggregate
    sum_of_workout = FitnessActivate.objects.filter(worked_at__date=datetime.date.today()).aggregate(burn=Sum('consumed_calories'))

    # 오늘 저장된 음식들의 칼로리 합계
    sum_of_food = IncomeFoods.objects.filter(income_at__date=datetime.date.today()).aggregate(
        ate=Sum('income_calories'))

    # HTTP GET POST PUT UPDATE DELETE
    if request.method == 'POST':  # 모두저장 눌렀을때
        # print(request.POST)
        count = request.POST.get('count_name')
        profile = Profile.objects.get(user=request.user.pk)  # 이거 수정함

        loop_count = 0
        for i in range(int(count)):
            loop_count += 1
            worked_out_name = 'worked_out_list_'+str(loop_count)
            print(worked_out_name)
            get_worked_out = request.POST.getlist(worked_out_name)
            print(get_worked_out)

            # ['1', '운동-2', '1', '150', '1500', '5', 'workout']
            # get_worked_out[6] ==  food or workout
            print(f"운동이름은 : {get_worked_out[1]} / 운동 PK는 : {get_worked_out[5]} / 운동시간은 : {get_worked_out[2]} / 소모칼로리는 : {get_worked_out[4]} 입니다.")

            if get_worked_out[6] == 'workout':

                creation = FitnessActivate.objects.create(
                    user=profile,  # 이거 수정함
                    fitness=FitnessSpec.objects.get(pk=int(get_worked_out[5])),
                    minute=int(get_worked_out[2]),
                    consumed_calories=int(get_worked_out[4])
                )
                creation.save()
            elif get_worked_out[6] == 'food':
                creation = IncomeFoods.objects.create(
                    user=profile,
                    food=FoodSpec.objects.get(pk=int(get_worked_out[5])),
                    portion=int(get_worked_out[2]),
                    income_calories=int(get_worked_out[4])
                )
                creation.save()
            else:
                print('get_worked_out[6]번이 workout도 아니고 food도 아님')
                print("-----------------------")
                print(get_worked_out[6])
                print("-----------------------")
                pass
        return redirect('calories_index')

    context = {
        'fitness': fitness,
        'foods': foods,
        'sum_of_workout': sum_of_workout,
        'sum_of_food': sum_of_food,
    }

    return render(request, 'calories/calories_index.html', context)


@login_required
def worked_detail(request):

    today_now = datetime.datetime.now()

    one_week_before = today_now - datetime.timedelta(weeks=1)

    print('++++++++++++++')
    print(today_now)
    print(one_week_before)
    print('++++++++++++++')

    recent_worked_out = FitnessActivate.objects.filter(
        user__user=request.user,
        worked_at__gte=one_week_before,
        # worked_at__lte=today_now
    )

    context = {
        'recent_worked_out': recent_worked_out
    }

    return render(request, 'calories/worked_detail.html', context)



# python API
# django-rest-framework <- stable little slow, document community
# django-ninja <- new release and fast

