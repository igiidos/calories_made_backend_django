from django.contrib.auth import views as auth_view
from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    # path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('logout/', views.Logout.as_view(), name='logout'),

]
