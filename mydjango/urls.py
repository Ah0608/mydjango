from user import views
from user.views import RegisterView, CheckUsernameView, Logoutview, IndexView, res_sendmeail, LoginView, ForgetPasswordView, \
    forget_sendmeail, ModifyPasswordView
from django.urls import path, include

urlpatterns = [
    path('index/', IndexView.as_view(),name='index'),
    path('register/', RegisterView.as_view(),name='register'),
    path("login/", LoginView.as_view(),name='login'),
    path("logout/", Logoutview.as_view(),name='logout'),
    path("register/sendmeail/", res_sendmeail,name='res_sendmeail'),
    path("forget/sendmeail/", forget_sendmeail,name='forget_sendmeail'),
    path('captcha/', include('captcha.urls'),name='captcha'),   # 增加这一行
    path('checkusername/', CheckUsernameView.as_view(), name='checkusername'),
    path('forgetpassword/', ForgetPasswordView.as_view(), name='forgetpassword'),
    path('modifypassword/', ModifyPasswordView.as_view(), name='modifypassword'),
]