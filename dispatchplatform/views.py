import json
import os
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.http.response import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.decorators.csrf import csrf_exempt
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJob

from common.check_proxy import multi_thread_check_proxy
from common.cmd_task import wrapper_my_job
from common.crawl_github_project import crawl_project_case
from common.crawl_proxy import crawl
from dispatchplatform.models import DisPlatform
from serializers.modelserializers import PlatformSerializer

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

github_trigger = CronTrigger.from_crontab('00 08 * * *')
scheduler.add_job(crawl_project_case, trigger=github_trigger, id='github_crawl', max_instances=5, replace_existing=True,)

crawl_trigger = CronTrigger.from_crontab('00 12 * * *')
scheduler.add_job(crawl, trigger=crawl_trigger, id='proxy_crawl', max_instances=5, replace_existing=True)

check_trigger = IntervalTrigger(hours=6)
scheduler.add_job(multi_thread_check_proxy, trigger=check_trigger, id='proxy_check', max_instances=5,
                  replace_existing=True, # multi_thread_check_proxy方法我已经注释掉
                  args=['https://www.baidu.com'])
scheduler.start()


class List(View):
    def get(self, request):
        current_time = datetime.now()
        # 查询date类型并删除早于当前时间的记录
        ran_id = None
        ran_task = DisPlatform.objects.filter(time_type='date', trigger_args__lt=current_time).first()
        if ran_task:
            ran_id = ran_task.job_id
        tasks = DisPlatform.objects.all()
        id_list = list(DjangoJob.objects.exclude(next_run_time__isnull=True).values_list('id', flat=True))
        time_qs = DjangoJob.objects.all().values_list('id', 'next_run_time')
        time_list = [{item[0]: item[1]} for item in time_qs]
        return render(request, 'displateformlist.html',
                      {'tasks': tasks, 'id_list': id_list, 'time_list': time_list, 'ran_id': ran_id})


@csrf_exempt
def Start(request):
    idlist = json.loads(request.POST.get('ids', ''))
    if not scheduler.running:
        scheduler.start()
    for job_id in idlist:
        task = DisPlatform.objects.filter(job_id=job_id).first()
        if task.time_type == 'date':
            trigger = DateTrigger(run_date=task.trigger_args)
            scheduler.add_job(wrapper_my_job, trigger=trigger, id=task.job_id, replace_existing=True, max_instances=5,
                              next_run_time=datetime.now(),
                              args=[task.task_file, task.python_path, task.job_id, task.env_variable])
        elif task.time_type == 'interval':
            trigger_obj = eval(task.trigger_args)
            trigger = IntervalTrigger(**trigger_obj)
            scheduler.add_job(wrapper_my_job, trigger=trigger, id=task.job_id, replace_existing=True, max_instances=5,
                              next_run_time=datetime.now(),
                              args=[task.task_file, task.python_path, task.job_id, task.env_variable])
        else:
            trigger = CronTrigger.from_crontab(task.trigger_args)
            scheduler.add_job(wrapper_my_job, trigger=trigger, id=task.job_id, max_instances=5, replace_existing=True,
                              next_run_time=datetime.now(),
                              args=[task.task_file, task.python_path, task.job_id, task.env_variable])
        DisPlatform.objects.filter(job_id=job_id).update(scheduler_state=True)
    return JsonResponse({'status': 'success'})


class Create(View):

    def post(self, requests):
        task_name = requests.POST.get('taskname', '')
        task_file = requests.POST.get('taskfile', '')
        job_id = requests.POST.get('job_id', '')
        time_type = requests.POST.get('select-option', '')
        python_path = requests.POST.get('python-path', '')
        env_variable = requests.POST.get('env-variable', '')
        if time_type == 'date':
            trigger_args = requests.POST.get('datetime_input', '')
        elif time_type == 'interval':
            trigger_args = {}
            num = int(requests.POST.get('num', ''))
            unit = requests.POST.get('unit', '')
            trigger_args[unit] = num
        else:
            trigger_args = requests.POST.get('timeexp', '')

        DisPlatform.objects.create(task_name=task_name, python_path=python_path, env_variable=env_variable,
                                   task_file=task_file, job_id=job_id, time_type=time_type, trigger_args=trigger_args)
        return JsonResponse({'status': 'success'})


@csrf_exempt
def Resume(request):
    idlist = json.loads(request.POST.get('ids', ''))
    if not scheduler.running:
        scheduler.start()
    for job_id in idlist:
        scheduler.resume_job(job_id)
    return JsonResponse({'status': 'success'})


@csrf_exempt
def Pause(request):
    idlist = json.loads(request.POST.get('ids', ''))
    if not scheduler.running:
        scheduler.start()
    for job_id in idlist:
        scheduler.pause_job(job_id)
    return JsonResponse({'status': 'success'})


@csrf_exempt
def Remove(request):
    idlist = json.loads(request.POST.get('ids', ''))
    if not scheduler.running:
        scheduler.start()
    for job_id in idlist:
        scheduler.remove_job(job_id)
        DisPlatform.objects.filter(job_id=job_id).delete()
    return JsonResponse({'status': 'remove OK'})


@csrf_exempt
def Modify(request):
    if request.method == 'POST':
        task_name = request.POST.get('taskname', '')
        task_file = request.POST.get('taskfile', '')
        job_id = request.POST.get('job_id', '')
        time_type = request.POST.get('select-option', '')
        python_path = request.POST.get('python-path', '')
        if time_type == 'date':
            trigger_args = request.POST.get('datetime_input', '')
            trigger = DateTrigger(run_date=trigger_args)
            scheduler.modify_job(job_id=job_id, trigger=trigger)
        elif time_type == 'interval':
            trigger_args = {}
            num = int(request.POST.get('num', ''))
            unit = request.POST.get('unit', '')
            trigger_args[unit] = num
            trigger = IntervalTrigger(**trigger_args)
            scheduler.modify_job(job_id=job_id, trigger=trigger)
        else:
            trigger_args = request.POST.get('timeexp', '')
            trigger = CronTrigger.from_crontab(trigger_args)
            scheduler.modify_job(job_id=job_id, trigger=trigger)
        DisPlatform.objects.filter(job_id=job_id).update(task_name=task_name, python_path=python_path,
                                                         task_file=task_file,
                                                         time_type=time_type, trigger_args=trigger_args)
        return redirect('platform_list')

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        job_id = request.GET.get('job_id')
        task = DisPlatform.objects.filter(job_id=job_id).first()
        serializer_task = PlatformSerializer(task).data
        return JsonResponse(serializer_task)


@csrf_exempt
def Search(request):
    if request.method == 'POST':
        inputValue = request.POST.get('search-task', '')
        tasks = DisPlatform.objects.filter(task_name__icontains=inputValue).all()
        id_list = list(
            DjangoJob.objects.filter(id=tasks.first().job_id).exclude(next_run_time__isnull=True).values_list('id',
                                                                                                              flat=True))
        time_qs = DjangoJob.objects.filter(id=tasks.first().job_id).values_list('id', 'next_run_time')
        time_list = [{item[0]: item[1]} for item in time_qs]
        return render(request, 'displateformlist.html', {'tasks': tasks, 'id_list': id_list, 'time_list': time_list})


def Viewlog(request, job_id):
    log_file_path = 'logs/log_{}/{}.log'.format(job_id, job_id)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
        return render(request, 'viewlog.html', {'log': log_content, 'job_id': job_id})
    else:
        return render(request, 'viewlog.html', {'job_id': job_id})


def Realtimelog(request, job_id):
    log_file_path = 'logs/log_{}/{}.log'.format(job_id, job_id)
    with open(log_file_path, 'r', encoding='utf-8') as file:
        log_content = file.read()
    return JsonResponse({'log': log_content})