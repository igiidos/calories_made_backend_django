from random import random, randrange

import requests
import json
from django.shortcuts import render

from calories.models import FitnessSpec


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


def calories_index(request):

    # count = 0
    # for i in range(20):
    #     spec = f'운동-{count}'  # 운동-0, 운동-1
    #     count += 1
    #     cal = randrange(1, 20)
    #
    #     obj = FitnessSpec.objects.create(
    #         spec=spec,
    #         calorie=cal
    #     )
    #     obj.save()

    fitness = FitnessSpec.objects.all()

    context = {
        'fitness': fitness
    }

    return render(request, 'calories/calories_index.html', context)

