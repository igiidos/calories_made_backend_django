import datetime
import json
import ast

from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Sum
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from api.serializer import ResultSerializer, ResultDicSerializer, ErrorSerializer
from calories.models import FoodSpec, FitnessSpec, FitnessActivate, IncomeFoods


class TestApi(APIView):

    def get(self, request):
        print("new api test")

        result = {
            'name': '김보리',
            'height': '2.1m',
            'weight': '60kg'
        }

        return Response(result, status=status.HTTP_200_OK)


test_api = TestApi.as_view()


class UserLists(APIView):
    def get(self, request):
        # url.com/?date_type=1
        # date_type=1 -> 오늘가입한 유져
        # date_type=2 -> 1주일간 가입한 유져
        # date_type=3 -> 한달간 가입한 유져
        # date_type=4 -> 언제부터~ 언제까지 가입한 유져
        # date_type=4 일때는 from 과 to 가 있어야 response
        # 안보내면 -> 전부다

        date_request = request.GET.get('date_type', None)

        date_now = datetime.datetime.now()
        today = date_now.today().date()  # 2021-09-01
        tomorrow = today + datetime.timedelta(days=1)

        before_a_week = today - datetime.timedelta(weeks=1)

        before_a_month = today - datetime.timedelta(days=30)

        if date_request and date_request == '1':
            lists = User.objects.filter(date_joined__range=(today, tomorrow)).values()
        elif date_request and date_request == '2':
            lists = User.objects.filter(date_joined__gte=before_a_week).values()
        elif date_request and date_request == '3':
            lists = User.objects.filter(date_joined__gte=before_a_month).values()
        elif date_request and date_request == '4':
            from_date = request.GET.get('from', None)
            to_date = request.GET.get('to', None)
            if from_date and to_date:
                lists = User.objects.filter(date_joined__gte=from_date, date_joined__lte=to_date).values()
            else:
                result = ErrorSerializer(
                    data={
                        'message': 'from_date and to_date are required!!',
                        'error': True
                    }
                )
                return Response(result.initial_data, status=status.HTTP_400_BAD_REQUEST)
        else:

            lists = User.objects.values()

        result = ResultSerializer(
            data={
                'message': 'successfully load all data',
                'resp': lists,
                'error': False
            }
        )

        return Response(result.initial_data, status=status.HTTP_200_OK)


user_lists = UserLists.as_view()


class FoodLists(APIView):
    def get(self, request):

        # lists = FoodSpec.objects.all()  # Type : queryset Type
        # lists = FoodSpec.objects.values_list()  # Type : array (List)
        lists = FoodSpec.objects.values()  # Type: key, value (dictionary)

        result = ResultSerializer(
            data={
                'message': 'successfully load all data',
                'resp': lists,
                'error': False
            }
        )

        # result = ResultSerializer(lists, many=True)  # 데이터가 한개만 가져오는것이면 many=False, 다수 이면 many=True

        return Response(result.initial_data, status=status.HTTP_200_OK)


food_lists = FoodLists.as_view()


class WorkoutLists(APIView):
    def get(self, request):

        # lists = FoodSpec.objects.all()  # Type : queryset Type
        # lists = FoodSpec.objects.values_list()  # Type : array (List)
        lists = FitnessSpec.objects.values()  # Type: key, value (dictionary)

        result = ResultSerializer(
            data={
                'message': 'successfully load all data',
                'resp': lists,
                'error': False
            }
        )

        # result = ResultSerializer(lists, many=True)  # 데이터가 한개만 가져오는것이면 many=False, 다수 이면 many=True

        return Response(result.initial_data, status=status.HTTP_200_OK)


workout_lists = WorkoutLists.as_view()


class MyWorkOut(APIView):
    # 127.0.0.1:8000/api/list/myworkout/4(Profile DB pk)/
    # 127.0.0.1:8000/api/list/myworkout/4/?month=202110
    # User_PK -> Profile(user=) -> FitnessActivate(user=)
    # 2021년10월것만
    # url string query에 month가 없으면 다보여주고
    # 있으면 그 월만 보여주게

    def get(self, request, pk):

        get_month = request.GET.get('month', None)  # month=202110

        if get_month:
            print(get_month)
            year = get_month[:4]  # 202110
            month = get_month[4:6]  # 2021 10
            lists = FitnessActivate.objects.filter(user__user=pk, worked_at__month=month, worked_at__year=year).values()
        else:
            print('None')
            lists = FitnessActivate.objects.filter(user__user=pk).values()

        sum_cal = 0
        for i in lists:
            sum_cal += i['consumed_calories']

        final = {
            'Total': sum_cal,
            'lists': lists
        }

        result = ResultDicSerializer(
            data={
                'message': 'successfully load all data',
                'resp': final,  # { key : value    }
                'error': False
            }
        )

        # result = ResultSerializer(lists, many=True)  # 데이터가 한개만 가져오는것이면 many=False, 다수 이면 many=True

        return Response(result.initial_data, status=status.HTTP_200_OK)

    def post(self, request, pk):  # <- This pk is for user's profile

        # user's profile pk, fitness, minute, consumed_calories, worked_at(auto)(X)

        get_save_type = request.data['type']  # 1. 1개만, 2. 여러개

        # type이 2로 오면
        # how to get data

        # [{'workout': 2, 'min': 10}, {'workout': 3, 'min': 20}, {'workout': 4, 'min': 30}]

        if get_save_type == 1 or get_save_type == '1':
            get_workout = request.data['workout']  # run(x), pk of run (o)
            get_minute = request.data['min']

            # if received 'get_burned' => use, if not calculate total_burned

            find_workout = FitnessSpec.objects.get(pk=int(get_workout))
            try:
                total_burned = request.data['consumed']  # optional
            except MultiValueDictKeyError as mde:  # consumed를 key로 받고있지 않을때
                total_burned = find_workout.calorie * get_minute

            except Exception as e:
                print(f'unknown error => {e}')
                result = ResultSerializer(
                    data={
                        'message': f'unknown error => {e}',
                        'resp': [],
                        'error': True
                    }
                )
                return Response(result.initial_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            saving = FitnessActivate.objects.create(
                user=Profile.objects.get(pk=pk),
                fitness=find_workout,
                minute=get_minute,
                consumed_calories=total_burned,
                # worked_at= (auto.. )
            )

            saving.save()

            render_list = serializers.serialize('json', [saving, ])

            # print(serializers.serialize('json', [saving, ]))

            result = ResultSerializer(
                data={
                    'message': 'successfully saved data',
                    'resp': render_list,
                    'error': False
                }
            )

            return Response(result.initial_data, status=status.HTTP_201_CREATED)

        elif get_save_type == 2 or get_save_type == '2':

            get_object_list = request.data['data_list']

            get_object_list = ast.literal_eval(get_object_list)

            print(type(get_object_list))
            print(get_object_list)

            for i in get_object_list:
                find_workout = FitnessSpec.objects.get(pk=int(i['workout']))

                saving = FitnessActivate.objects.create(
                    user=Profile.objects.get(pk=pk),
                    fitness=find_workout,
                    minute=i['min'],
                    consumed_calories=find_workout.calorie * i['min'],
                    # worked_at= (auto.. )
                )

                saving.save()

                # render_list = serializers.serialize('json', [saving, ])

                # print(serializers.serialize('json', [saving, ]))

            result = ResultSerializer(
                data={
                    'message': 'successfully saved data',
                    'resp': [],
                    'error': False
                }
            )

            return Response(result.initial_data, status=status.HTTP_201_CREATED)

        else:
            result = ErrorSerializer(
                data={
                    'message': 'type is invalid',
                    'error': True
                }
            )
            return Response(result.initial_data, status=status.HTTP_400_BAD_REQUEST)


myworkout_list = MyWorkOut.as_view()


class MyDiet(APIView):

    def get(self, request, pk):

        get_month = request.GET.get('month', None)  # month=202110

        if get_month:
            print(get_month)
            year = get_month[:4]  # 202110
            month = get_month[4:6]  # 2021 10
            lists = IncomeFoods.objects.filter(user__user=pk, income_at__month=month, income_at__year=year).values()
        else:
            print('None')
            lists = IncomeFoods.objects.filter(user__user=pk).values()

        sum_cal = 0
        for i in lists:
            sum_cal += i['income_calories']

        final = {
            'Total': sum_cal,
            'lists': lists
        }

        result = ResultDicSerializer(
            data={
                'message': 'successfully load all data',
                'resp': final,
                'error': False
            }
        )

        return Response(result.initial_data, status=status.HTTP_200_OK)

    def post(self, request, pk):  # <- This pk is for user's profile

        # user's profile pk, fitness, minute, consumed_calories, worked_at(auto)(X)

        get_save_type = request.data['type']  # 1. 1개만, 2. 여러개

        # type이 2로 오면
        # how to get data

        # [{'food': 2, 'portion': 1}, {'workout': 3, 'min': 20}, {'workout': 4, 'min': 30}]

        if get_save_type == 1 or get_save_type == '1':
            get_food = request.data['food']  # run(x), pk of run (o)
            get_portion = request.data['portion']

            # if received 'get_burned' => use, if not calculate total_burned

            find_food = FoodSpec.objects.get(pk=int(get_food))

            try:
                total = request.data['consumed']  # optional
            except MultiValueDictKeyError as mde:  # consumed를 key로 받고있지 않을때
                total = find_food.calorie * int(get_portion)

            except Exception as e:
                print(f'unknown error => {e}')
                result = ResultSerializer(
                    data={
                        'message': f'unknown error => {e}',
                        'resp': [],
                        'error': True
                    }
                )
                return Response(result.initial_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            saving = IncomeFoods.objects.create(
                user=Profile.objects.get(pk=pk),
                food=find_food,
                portion=get_portion,
                income_calories=total,
                # income_at= (auto.. )
            )

            saving.save()

            render_list = serializers.serialize('json', [saving, ])

            # print(serializers.serialize('json', [saving, ]))

            result = ResultSerializer(
                data={
                    'message': 'successfully saved data',
                    'resp': render_list,
                    'error': False
                }
            )

            return Response(result.initial_data, status=status.HTTP_201_CREATED)

        elif get_save_type == 2 or get_save_type == '2':

            get_object_list = request.data['data_list']

            get_object_list = ast.literal_eval(get_object_list)

            print(type(get_object_list))
            print(get_object_list)

            for i in get_object_list:
                find_food = FoodSpec.objects.get(pk=int(i['food']))

                saving = IncomeFoods.objects.create(
                    user=Profile.objects.get(pk=pk),
                    food=find_food,
                    portion=i['portion'],
                    income_calories=find_food.calorie * i['portion'],
                    # worked_at= (auto.. )
                )

                saving.save()

                # render_list = serializers.serialize('json', [saving, ])

                # print(serializers.serialize('json', [saving, ]))

            result = ResultSerializer(
                data={
                    'message': 'successfully saved data',
                    'resp': [],
                    'error': False
                }
            )

            return Response(result.initial_data, status=status.HTTP_201_CREATED)

        else:
            result = ErrorSerializer(
                data={
                    'message': 'type is invalid',
                    'error': True
                }
            )
            return Response(result.initial_data, status=status.HTTP_400_BAD_REQUEST)




mydiet_list = MyDiet.as_view()

# 운동한 리스트와 합계
# 먹은 리스트와 합계
# 운동한 리스트와 운동합계 그리고 먹은 리스트와 먹은 합계 그리고~~~ 전부다합계


class MyHealth(APIView):

    def get(self, request, pk):

        get_month = request.GET.get('month', None)  # month=202110

        if get_month:
            print(get_month)
            year = get_month[:4]  # 202110
            month = get_month[4:6]  # 2021 10
            food_lists = IncomeFoods.objects.filter(user__user=pk, income_at__month=month, income_at__year=year).values()
            workout_lists = FitnessActivate.objects.filter(user__user=pk, worked_at__month=month, worked_at__year=year).values()
        else:
            print('None')
            food_lists = IncomeFoods.objects.filter(user__user=pk).values()
            workout_lists = FitnessActivate.objects.filter(user__user=pk).values()

        sum_food_cal = 0
        for i in food_lists:
            sum_food_cal += i['income_calories']

        sum_workout_cal = 0
        for i in workout_lists:
            sum_workout_cal += i['consumed_calories']

        final = {
            'Total': sum_food_cal - sum_workout_cal,
            'food_total': sum_food_cal,
            'workout_total': sum_workout_cal,
            'food_lists': food_lists,
            'workout_lists': workout_lists,
        }

        result = ResultDicSerializer(
            data={
                'message': 'successfully load all data',
                'resp': final,
                'error': False
            }
        )

        return Response(result.initial_data, status=status.HTTP_200_OK)


myhealth_list = MyHealth.as_view()


class SearchWorkout(APIView):

    def get(self, request):

        get_words = request.GET.get('words', None)

        print(get_words)

        if get_words:

            get_object = FitnessSpec.objects.filter(spec__icontains=get_words).values()

            print(get_object)

            result = ResultSerializer(
                data={
                    'message': 'successfully load all data',
                    'resp': get_object,
                    'error': False
                }
            )

            # result = ResultSerializer(lists, many=True)  # 데이터가 한개만 가져오는것이면 many=False, 다수 이면 many=True

            return Response(result.initial_data, status=status.HTTP_200_OK)

        else:
            result = ErrorSerializer(
                data={
                    'message': 'search words is required',
                    'error': True
                }
            )
            return Response(result.initial_data, status=status.HTTP_400_BAD_REQUEST)


search_workout = SearchWorkout.as_view()


class SearchFood(APIView):

    def get(self, request):

        get_words = request.GET.get('words', None)

        if get_words:

            get_object = FoodSpec.objects.filter(spec__icontains=get_words).values()

            result = ResultSerializer(
                data={
                    'message': 'successfully load all data',
                    'resp': get_object,
                    'error': False
                }
            )

            # result = ResultSerializer(lists, many=True)  # 데이터가 한개만 가져오는것이면 many=False, 다수 이면 many=True

            return Response(result.initial_data, status=status.HTTP_200_OK)

        else:
            result = ErrorSerializer(
                data={
                    'message': 'search words is required',
                    'error': True
                }
            )
            return Response(result.initial_data, status=status.HTTP_400_BAD_REQUEST)


search_food = SearchFood.as_view()


# 헬스 운동 => 칼로리 세트 무게, 몸무게 등등 구분해서 어떻게 계산해야 하는지
# 목업 한페이지 할때마다 삼촌이랑 상의

# 다음주 회원가입, 로그인 등 auth
# google login, facebook login
# react-native 프레임워크 앱 개발 => 80% javascript, 10% java(Android), 10% Object-C(Swift)
