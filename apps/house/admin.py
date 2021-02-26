from django.contrib import admin
from house.models import HouseInfo, HouseType, Area, HouseImage, House_Facility, IndexHouseBanner


# Register your models here.
class baseAdmin(admin.ModelAdmin):
    list_per_page = 50


# 关联对象
class HouseTypeInline(admin.TabularInline):
    model = HouseType
    extra = 2


class HouseFacilityInline(admin.TabularInline):
    model = House_Facility
    extra = 2


class ImagesInline(admin.TabularInline):
    model = HouseImage
    extra = 2


class HouseInfoAdmin(baseAdmin):
    '''房子信息管理类'''
    list_display = ['id', 'title', 'area', 'price', 'comment_count', 'isBook']
    list_filter = ['area']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'price', 'addr']
    # 添加页面显示字段
    fields = ['title', 'area', 'addr', 'price', 'min_stay_day', 'max_stay_day', 'user', 'image', 'comment_count', 'isBook']
    inlines = [HouseTypeInline, HouseFacilityInline, ImagesInline]



class HouseFacilityAdmin(baseAdmin):
    '''房子配套设备管理类'''
    list_display = ['house', 'facility']
    fields = ['house', 'facility']
    search_fields = ['house__title__icontains', 'facility']


class HouseTypeAdmin(baseAdmin):
    list_display = ['house', 'type_name', 'type']
    fields = ['house', 'type_name', 'type']
    search_fields = ['house__title__icontains', 'type']

class AreaAdmin(baseAdmin):
    pass


class ImageAdmin(baseAdmin):
    pass


class bannerAdmin(baseAdmin):

    fields = ['house', 'title', 'index']


admin.site.register(HouseInfo, HouseInfoAdmin)
admin.site.register(HouseType, HouseTypeAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(HouseImage, ImageAdmin)
admin.site.register(House_Facility, HouseFacilityAdmin)
admin.site.register(IndexHouseBanner, bannerAdmin)
