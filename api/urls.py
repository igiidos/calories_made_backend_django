from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test_api),
    path('list/user/', views.user_lists),
    path('list/food/', views.food_lists),
    path('list/workout/', views.workout_lists),
    path('list/myworkout/<pk>/', views.myworkout_list),
    path('list/mydiet/<pk>/', views.mydiet_list),
    path('list/myhealth/<pk>/', views.myhealth_list),

]

