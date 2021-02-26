from django.contrib import admin
from order.models import Comment, order


# Register your models here.
class baseAdmin(admin.ModelAdmin):
    list_per_page = 50


class orderAdmin(baseAdmin):
    list_display = ['order_id', 'user', 'house', 'inTime', 'outTime', 'orderStatue']
    search_fields = ['order_id', 'user__username__icontains', 'house__title__icontains']


class commentAdmin(baseAdmin):
    list_display = ['user', 'house', 'comment']
    search_fields = ['user__username__icontains', 'house__title__icontains']


admin.site.register(Comment, commentAdmin)
admin.site.register(order, orderAdmin)
