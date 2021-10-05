import datetime
from random import random, randrange

import requests
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Profile
from calories.models import FitnessSpec, FitnessActivate, FoodSpec, IncomeFoods


def search_food(request):

    get_food = request.GET.get('food', None)
    print(get_food)

    # if get_food:
    #     food_name = get_food
    # else:
    #     food_name = '바나나칩'

    url = 'http://apis.data.go.kr/1470000/FoodNtrIrdntInfoService/getFoodNtrItdntList'
    params = {
        'ServiceKey': 'BsfQgS+zkc2qI2dw8Aiyx/F106HRcpOi8SpPkMOJ1wT3jp1cGZnKSI7BIB6zzY48ciAI3ieVx2Ctq3qz+8ltdg==',
        # 'numOfRows': 3,
        'pageNo': 1,
        'type': 'json',
        'desc_kor': get_food
    }

    food_list = requests.get(url, params=params)

    if food_list.status_code != 200:
        foods = None

    else:
        food = food_list.json()

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
                    user=profile, # 이거 수정함
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

    context = {
        'fitness': fitness,
        'foods': foods
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
