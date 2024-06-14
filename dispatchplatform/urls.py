from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.List.as_view(), name='platform_list'),
    path('start/<int:pk>/', views.Start, name='platform_start'),
    path('create/', views.Create.as_view(), name='platform_create'),
    path('resume/<int:job_id>/', views.Resume, name='platform_resume'),
    path('pause/<int:job_id>/', views.Pause, name='platform_pause'),
    path('remove/<int:job_id>/', views.Remove, name='platform_remove'),
    path('modify/', views.Modify, name='platform_modify'),
    path('search/', views.Search, name='platform_search'),
    path('viewlog/<int:job_id>/', views.Viewlog, name='viewlog'),
    path('realtimelog/<int:job_id>/', views.Realtimelog, name='realtimelog'),
]