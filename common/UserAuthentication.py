from datetime import timedelta

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import User


class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user and user.check_password(password):
            # 如果用户名或邮箱和密码匹配成功，则设置会话的过期时间为7天
            request.session.set_expiry(timedelta(hours=24 * 7).seconds)
            return user
        return None
