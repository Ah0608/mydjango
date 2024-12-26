import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from plan.forms import DailyReportForm
from plan.models import DailyReport


class Calendar(View):

    def get(self, request):
        ret = dict()
        category_all = [{'key': i[0], 'value': i[1]} for i in DailyReport.cat_choices]
        my_report_all = DailyReport.objects.filter(user=request.user.id)
        ret['my_report_all'] = my_report_all
        ret['category_all'] = category_all
        return render(request, 'calendar.html', ret)


class Calendarcreate(View):

    def post(self, request):
        res = dict(result=False)
        daily_report_form = DailyReportForm(request.POST)
        if daily_report_form.is_valid():
            daily_report_form.save()
            res['status'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class ReportDetailView(View):
    """
    日报详情：用于日历展示日报详情和修改日报内容
    """
    def get(self, request, pk):
        report = DailyReport.objects.filter(id=pk).first()
        # form = DailyReportForm(instance=report)
        category_all = [{'key': i[0], 'value': i[1]} for i in DailyReport.cat_choices]
        user = request.user
        return render(request, 'calendardetail.html', {'report': report, 'user': user, 'category_all': category_all})

    def post(self, request, pk):
        article = DailyReport.objects.filter(id=pk).first()

        form = DailyReportForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('calendar')


class ReportDeleteView(View):

    def get(self,request,pk):
        obj = DailyReport.objects.filter(id=pk)
        obj.delete()
        return redirect('calendar')


