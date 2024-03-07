from django.contrib import admin

# Register your models here.
from .models import Reguser, Category, Bloginfo, Tag


class BloginfoAdmin(admin.ModelAdmin):
    list_display = ('title','create_time','modified_time','category','author', 'views')


admin.site.register(Reguser)
admin.site.register(Category)
admin.site.register(Bloginfo, BloginfoAdmin)
admin.site.register(Tag)
