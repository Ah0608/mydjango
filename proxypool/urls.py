from django.urls import path

from proxypool.views import Proxypool, CheckProxy, AllProxy, RandomProxy, DeleteProxy

urlpatterns = [
    path('proxylist/', Proxypool.as_view(), name='proxypool'),
    path('checkproxy/', CheckProxy, name='checkproxy'),
    path('allproxy/', AllProxy.as_view(), name='allproxy'),
    path('randomproxy/', RandomProxy.as_view(), name='randomproxy'),
    path('deleteproxy/', DeleteProxy, name='deleteproxy'),
]
