from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test_api),
    path('list/food/', views.food_lists),
    # path('search_food/', views.search_food, name='search_food'),
    # path('calories_index/', views.calories_index, name='calories_index'),
    # path('worked_out/detail/', views.worked_detail, name='worked_detail'),
]

