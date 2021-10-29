from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry        # 操作日志

from .adminforms import PostAdminForm
from .models import Post, Category, Tag

from typeidea.custom_site import custom_site        #自定义site
from typeidea.base_admin import BaseOwnerAdmin
# Register your models here.


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'post_count', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')
    
    # 写在了BaseOwnerAdmin中,后面的class同理
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    """ 文章数量 """
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


""" 自定义过滤器只显示当前用户分类 """
class CategoryOwnFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

@admin.register(Post, site=custom_site)     # site=custom_site 自定义的site，同时修改了下面revers中的admin->cus_admin
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm            # 文章内容中的 '摘要' 部分变成自定义的样式，在adminforms.py中

    list_display = [
        'title', 'category', 'status', 'created_time', 'owner', 'operator'
    ]
    list_display_links = []         # 那些字段可以作为链接
    
    list_filter = [CategoryOwnFilter]   # 已设置为显示当前用户分类[CategoryOwnFilter]，开放所有：['category', ]
    search_fields = ['title', 'category__name']
    
    actions_on_top = True
    actions_on_bottom = True
    
    #编辑页面
    save_on_top = True

    exclude = ('owner', )       # 不展示的字段

    """    
    fields = (
            ('category', 'title'),
            'desc',
            'status',
            'content',
            'tag',
        )
    """

    # 自定义field样式，代替原有fields
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse', ),      # 支持collapse（折叠） 或者 wide(展开)
            'fields': ('tag', ),
        }),
    )
    # filter_horizontal = ('tag', )         # 多对多的样式 filter_horizontal 横向；filter_vertical 纵向

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message', ]

