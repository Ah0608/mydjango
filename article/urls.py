from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.article_list, name='article_list'),
    path('create/', views.article_create, name='article_create'),
    path('detail/<int:pk>/', views.article_detail, name='article_detail'),
    path('edit/<int:pk>/', views.article_edit, name='article_edit'),
    path('delete/<int:pk>/', views.article_delete, name='article_delete'),
    path('search/', views.article_search, name='article_search'),
]