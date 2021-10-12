import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer import ResultSerializer
from calories.models import FoodSpec


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


