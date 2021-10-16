import json

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer import ResultSerializer
from calories.models import FoodSpec, FitnessSpec, FitnessActivate


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

        result = ResultSerializer(
            data={
                'message': 'successfully load all data',
                'resp': lists,
                'error': False
            }
        )

        # result = ResultSerializer(lists, many=True)  # 데이터가 한개만 가져오는것이면 many=False, 다수 이면 many=True

        return Response(result.initial_data, status=status.HTTP_200_OK)


myworkout_list = MyWorkOut.as_view()
