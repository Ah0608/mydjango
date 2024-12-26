from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.List.as_view(), name='platform_list'),
    path('start/', views.Start, name='platform_start'),
    path('create/', views.Create.as_view(), name='platform_create'),
    path('resume/', views.Resume, name='platform_resume'),
    path('pause/', views.Pause, name='platform_pause'),
    path('remove/', views.Remove, name='platform_remove'),
    path('modify/', views.Modify, name='platform_modify'),
    path('search/', views.Search, name='platform_search'),
    path('viewlog/<str:job_id>/', views.Viewlog, name='viewlog'),
    path('realtimelog/<str:job_id>/', views.Realtimelog, name='realtimelog'),
]