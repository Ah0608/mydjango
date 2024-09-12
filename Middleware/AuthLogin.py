# _*_ coding : utf-8 _*_
# @Time : 2024/4/4 0004 16:00
# @Author :HuangPeng
# @File : login_middleware
# @Project : mydjango
import re

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

AuthLogin_list = ['/article/','/plan/','/dispatchplatform/','/tools/']  # 需要登录认证的路由


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if any(re.match(r'^{}'.format(pattern), request.path) for pattern in AuthLogin_list):
            if not request.user.is_authenticated:
                return redirect('/login/')
