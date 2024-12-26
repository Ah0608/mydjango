import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.check_proxy import multi_thread_check_proxy
from common.get_ip import get_client_ip
from common.my_paginator import pg
from proxypool.models import ProxyPool
from serializers.modelserializers import ProxySerializer
from loguru import logger


class Proxypool(View):

    def get(self, request):
        client_ip = get_client_ip(request)
        logger.info(f"Client IP: {client_ip}")
        user = request.user
        queryset = ProxyPool.objects.all().order_by('speed')
        page_obj, page_range = pg(queryset, request, 10)

        return render(request, 'proxy.html', {'page_obj': page_obj, 'page_range': page_range, 'user': user})


@csrf_exempt
def CheckProxy(request):
    check_url = request.POST.get('url', '')
    multi_thread_check_proxy(check_url)
    return JsonResponse({'status': 200, 'message': 'ok'})


class AllProxy(View):

    def get(self, request):
        client_ip = get_client_ip(request)
        logger.info(f"Client IP: {client_ip}")
        try:
            queryset = ProxyPool.objects.all().order_by('speed')
            serializer = ProxySerializer(instance=queryset, many=True)
            proxy_list = [item['type'] + '://' + item['ip'] for item in serializer.data]
            return JsonResponse({'status': 200, 'data': proxy_list})
        except:
            return JsonResponse({'status': 500, 'message': []})


class RandomProxy(View):

    def get(self, request):
        client_ip = get_client_ip(request)
        logger.info(f"Client IP: {client_ip}")
        try:
            queryset = ProxyPool.objects.filter(speed__lt=4).order_by('speed')
            serializer = ProxySerializer(instance=queryset, many=True)
            proxy_list = [item['type'] + '://' + item['ip'] for item in serializer.data]
            random_proxy = random.choice(proxy_list)
            return HttpResponse(random_proxy)
        except:
            return HttpResponse('')


@csrf_exempt
def DeleteProxy(request):
    del_id = request.POST.get('del_id', '')
    ProxyPool.objects.filter(pk=del_id).delete()
    return JsonResponse({'status': 200, 'message': 'ok'})
