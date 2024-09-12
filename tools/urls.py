from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.List, name='toollist'),
    path('curl/', views.Curl, name='curl'),
    path('getweather/', views.getweather, name='getweather'),
    path('josnformat/', views.Josnformat, name='josnformat'),

]

