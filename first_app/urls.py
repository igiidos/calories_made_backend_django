from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<pk>/', views.post_detail, name='post_detail'),
    path('write/', views.post_write, name='post_write'),
    path('update/<pk>/', views.post_update, name='post_update'),
    path('delete/<pk>/', views.post_delete, name='post_delete'),
    path('ajax_study/', views.ajax_study, name='ajax_study'),
    path('text_data_ajax/', views.text_data_ajax, name='text_data_ajax')
]

