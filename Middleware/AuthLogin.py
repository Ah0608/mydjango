# _*_ coding : utf-8 _*_
# @Time : 2024/4/4 0004 16:00
# @Author :HuangPeng
# @File : login_middleware
# @Project : mydjango
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

AuthLogin_list = ['/index/'] #需要登录认证的路由


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path in AuthLogin_list:
            if not request.session.get('is_login', None):
                return redirect('/login/')

