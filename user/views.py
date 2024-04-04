import datetime
import random
import re
import time

from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.forms import LoginForm, RegisterForm, ForgetForm
from user.models import EmailVerify,User
from mydjango.settings import EMAIL_HOST_USER


class IndexView(View):
    def get(self, request):
        if not request.session.get('is_login', None):
            return redirect('/login/')
        return render(request, 'index.html', locals())


@csrf_exempt
def res_sendmeail(request):  # 注册
    if request.method == 'POST':
        email = request.POST.get('email')
        email_object = User.objects.filter(email=email)
        if email_object:
            message = '您填写的邮箱已注册'
            return JsonResponse({'flag': False, 'message': message})
        random_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        subject = 'Awesome后台系统用户注册'
        message = '''
        您好！
            欢迎注册Awesome后台系统，您的注册验证码为：{}
            该验证码有效时间为五分钟，请及时进行验证。

        Awesome开发团队
        '''.format(random_code)
        try:
            send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[email, ])
            EmailVerify.objects.filter(email_address=email).update(is_used=False)
            current_time = datetime.datetime.now()
            five_minutes_later = current_time + datetime.timedelta(minutes=5)
            five_minutes_later_timestamp = int(five_minutes_later.timestamp())
            EmailVerify.objects.create(email_address=email, verify_code=random_code,
                                       expiration_time=five_minutes_later_timestamp, is_used=True)
            message = '验证码发送成功'
            return JsonResponse({'flag': True, 'message': message})
        except Exception as e:
            print(e)
            message = '验证码发送失败'
            return JsonResponse({'flag': False, 'message': message})


@csrf_exempt
def forget_sendmeail(request):  # 重置密码
    if request.method == 'POST':
        email = request.POST.get('email')
        email_object = User.objects.filter(email=email)
        if not email_object:
            message = '您填写的邮箱还未注册'
            return JsonResponse({'flag': False, 'message': message})
        username = email_object.first().username
        random_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        subject = 'Awesome后台系统用户重置密码'
        message = '''
        用户{}，您好！
            您重置的验证码为：{}
            切勿把验证码泄露给他人，该验证码有效时间为五分钟，请及时进行验证。
            如非本人操作，请忽略本次短信。

        Awesome开发团队
        '''.format(username, random_code)
        try:
            send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[email, ])
            EmailVerify.objects.filter(email_address=email).update(is_used=False)
            current_time = datetime.datetime.now()
            five_minutes_later = current_time + datetime.timedelta(minutes=5)
            five_minutes_later_timestamp = int(five_minutes_later.timestamp())
            EmailVerify.objects.create(email_address=email, verify_code=random_code,
                                       expiration_time=five_minutes_later_timestamp, is_used=True)
            message = '验证码发送成功'
            return JsonResponse({'flag': True, 'message': message})
        except Exception as e:
            print(e)
            message = '验证码发送失败'
            return JsonResponse({'flag': False, 'message': message})


class Logoutview(View):
    def get(self, request):
        request.session.flush()  # 清除session数据
        return redirect('/login/')


class CheckUsernameView(View):
    def get(self, request):
        username = request.GET.get('username', None)
        pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9]{1,30}$'
        data = dict()
        if re.search(pattern, username):
            if User.objects.filter(username=username).exists():
                data['flag'] = False
                data['message'] = '该用户名已存在'
            else:
                data['flag'] = True
                data['message'] = '该用户名可用'
        else:
            data['flag'] = False
            data['message'] = '用户名只能包含汉字、数字和英文'
        return JsonResponse(data)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password_new = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(Q(username=username) | Q(email=username))
            except:
                messages.error(request, '您输入的账号不存在')
                return render(request, 'login.html', {'login_form': login_form})
            if check_password(password_new, user.password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                request.session.set_expiry(1 * 12 * 3600)
                time.sleep(2)
                return redirect('index')
            else:
                messages.error(request, '您的输入密码有误')
                return render(request, 'login.html', {'login_form': login_form})
        else:
            # 处理表单验证失败的情况
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)  # 把注册表单的数据引过来
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            confirm_pwd = register_form.cleaned_data.get('confirm_pwd')
            email = register_form.cleaned_data.get('email')
            verifycode = register_form.cleaned_data.get('verifycode')
            try:
                email_object = EmailVerify.objects.get(email_address=email, verify_code=verifycode, is_used=True)
                current_timestamp = int(time.time())
                if email_object.expiration_time - current_timestamp < 0:
                    messages.error(request, '验证码失效，请重新发送')
                    return render(request, 'register.html', locals())
            except:
                messages.error(request, '验证码有误，请重新输入')
                return render(request, 'register.html', locals())
            new_user = User()
            new_user.username = username
            new_user.password = make_password(password, salt='sc')
            new_user.email = email
            new_user.save()
            EmailVerify.objects.filter(email_address=email).update(is_used=False)
            time.sleep(1)
            return redirect('login')
        else:
            return render(request, 'register.html', locals())


class ForgetPasswordView(View):

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forget.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)  # 把注册表单的数据引过来
        if forget_form.is_valid():
            email = forget_form.cleaned_data.get('email')
            verifycode = forget_form.cleaned_data.get('verifycode')
            try:
                email_object = EmailVerify.objects.get(email_address=email, verify_code=verifycode, is_used=True)
                current_timestamp = int(time.time())
                if email_object.expiration_time - current_timestamp < 0:
                    messages.error(request, '验证码失效，请重新发送')
                    return render(request, 'forget.html', locals())
            except:
                messages.error(request, '验证码有误，请重新输入')
                return render(request, 'forget.html', locals())
            EmailVerify.objects.filter(email_address=email).update(is_used=False)
            time.sleep(1)
            return render(request, 'modify.html', {'email': email})
        else:
            return render(request, 'forget.html', locals())


class ModifyPasswordView(View):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        new_password = make_password(password)
        user.password = new_password
        user.save()
        time.sleep(1)
        return redirect('login')
