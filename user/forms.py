
from captcha.fields import CaptchaField
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25,label='账号',widget=forms.TextInput())
    password = forms.CharField(label="密码",max_length=16,min_length=8, widget=forms.PasswordInput())
    captcha = CaptchaField(label='验证码')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': '请输入{}'.format(field.label),
                'id': name
            })


class RegisterForm(forms.Form):

    username = forms.CharField(label='用户名',max_length=16,widget=forms.TextInput())

    password = forms.CharField(label='密码',max_length=16,min_length=8,widget=forms.PasswordInput())

    confirm_pwd = forms.CharField(label='确认密码', max_length=16,min_length=8,widget=forms.PasswordInput())

    email = forms.EmailField(label='邮箱',max_length=30,widget=forms.EmailInput())

    verifycode = forms.CharField(label='验证码',max_length=6,widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': '请输入{}'.format(field.label),
                'id': name
            })


class ForgetForm(forms.Form):

    email = forms.EmailField(label='邮箱',max_length=30,widget=forms.EmailInput())

    verifycode = forms.CharField(label='验证码',max_length=6,widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(ForgetForm, self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': '请输入{}'.format(field.label),
                'id': name
            })


class ModifyForm(forms.Form):

    password = forms.CharField(label='密码',max_length=16,min_length=8,widget=forms.PasswordInput())

    confirm_pwd = forms.CharField(label='确认密码', max_length=16,min_length=8,widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ModifyForm, self).__init__(*args, **kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': '请输入{}'.format(field.label),
                'id': name
            })