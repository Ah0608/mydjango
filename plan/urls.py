from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.Calendar.as_view(), name='calendar'),
    path('create/', views.Calendarcreate.as_view(), name='calendar_create'),
    path('detail/<int:pk>/', views.ReportDetailView.as_view(), name='calendar_detail'),
    path('delete/<int:pk>/', views.ReportDeleteView.as_view(), name='calendar_delete'),
]