from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Model


class Reguser(AbstractUser):

    nikename = models.CharField(max_length=32, verbose_name="昵称")

    telephone = models.CharField(max_length=11, unique=True, null=True,verbose_name="手机号")

    head_img = models.ImageField(upload_to="head_img/%Y/%m", default="head_img/default.png", max_length=100, verbose_name="头像")


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Bloginfo(models.Model):

    title = models.CharField(max_length=32, verbose_name="标题")
    body = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField( verbose_name="创建时间")
    modified_time = models.DateTimeField( verbose_name="修改时间")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True, verbose_name="分类")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="标签")
    author = models.ForeignKey(Reguser, on_delete=models.CASCADE, verbose_name="作者")
    views = models.PositiveIntegerField(default=0, verbose_name="浏览量")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time',]
        verbose_name = "文章"
        verbose_name_plural = verbose_name



class Category(models.Model):
    name = models.CharField(max_length=32,verbose_name="分类名称")
    desc = models.CharField(max_length=32,verbose_name="分类描述",null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=32,verbose_name="标签名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name