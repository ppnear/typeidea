# 定制site实现系统对外提供多套admin后台的逻辑，继承AdminSite定义自己的site

from django.contrib.admin import AdminSite

class CustomSide(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea管理后台'
    index_title = '首页'

custom_site = CustomSide(name='cus_admin')