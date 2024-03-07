from django import forms
from . import models
from django.core.exceptions import ValidationError


class reg_form(forms.Form):
    username = forms.CharField(
        max_length=20,
        label="账号",
        error_messages={
            "max_length": "账号最长20位",
            "required": "账号必输",
            "min_length": "账号最短6位"
        },
        # <input type='text'/>
        widget=forms.widgets.TextInput(
            attrs={'class': "form-control"},
        )
    )

    password = forms.CharField(
        max_length=6,
        label="密码",
        error_messages={
            "min_length": "密码最短6位",
            "required": "密码不能为空",
            "max_length": "密码最长20位"
        },
        # <input type='password'/>
        widget=forms.widgets.PasswordInput(
            attrs={'class': "form-control"},
        )
    )

    repassword = forms.CharField(
        max_length=6,
        label="确认密码",
        error_messages={
            "min_length": "密码最短6位",
            "required": "密码不能为空"
        },
        # <input type='password'/>
        widget=forms.widgets.PasswordInput(
            attrs={'class': "form-control"},
        )
    )

    nikename = forms.CharField(
        max_length=20,
        label="昵称",
        error_messages={
            "max_length": "昵称最大20字",
        },
        initial="王振兴",
        widget=forms.widgets.TextInput(
            attrs={'class': "form-control"},
        )
    )

    email = forms.EmailField(
        label="邮箱",
        error_messages={
            "invalid": "请输入正确的邮箱",
            "required": "邮箱不能为空",
        },
        widget=forms.widgets.EmailInput(
            attrs={'class': "form-control"},
        )
    )

    telephone = forms.CharField(
        label="电话",
        required=False,
        error_messages={
            'max_length': "手机号11位"
        },
        widget=forms.widgets.TextInput(
            attrs={'class': "form-control"},
        )
    )

    head_img = forms.ImageField(
        label="头像",
        widget = forms.widgets.FileInput(
            attrs={'style': "display:none"},
        )
    )

    # 确认密码和密码一致性检查
    def clean_repassword(self):
        passwd = self.cleaned_data.get('password')
        repasswd = self.cleaned_data.get('repassword')
        if repasswd and repasswd != passwd:
            self.add_error("repassword", ValidationError("两次输入密码不一致"))
        else:
            return repasswd

    # username存在性
    def clean_username(self):
        input_user = self.cleaned_data.get('username')

        # ORM
        user = models.Reguser.objects.filter(username=input_user)
        if user:
            self.add_error("username", ValidationError("用户账号已注册."))
        else:
            return input_user

    # def clean(self):
    #     self.cleaned_data

    # django 表单检查的顺序 is_valid() clean_xxx clean
    # 1.检查基础规则
    # 2.clean_xxx
    # 3.clean
