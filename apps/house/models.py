from django.db import models
from db.base_model import BaseModel


# Create your models here.
class Area(BaseModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name='地区')

    class Meta:
        db_table = 'mak_Area'
        verbose_name = '地区'
        verbose_name_plural = verbose_name


class HouseInfo(BaseModel):
    def __str__(self):
        return self.title

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='标题')
    price = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='价格')
    addr = models.CharField(max_length=256, verbose_name='房子地址')
    area = models.ForeignKey('Area', verbose_name='地区', on_delete=models.CASCADE)
    min_stay_day = models.CharField(max_length=10, verbose_name='最短入住天数', default='1')
    max_stay_day = models.CharField(max_length=10, verbose_name='最长入住天数', default='无限制')
    image = models.ImageField(upload_to='house', verbose_name='首页列表展示图')
    comment_count = models.IntegerField(verbose_name='评论数')
    isBook = models.BooleanField(default=False, verbose_name='是否有人入住')

    class Meta:
        db_table = 'mak_house'
        verbose_name = '房子'
        verbose_name_plural = verbose_name


class HouseType(BaseModel):
    def __str__(self):
        return self.house.title

    DISPLAY_TYPE_CHOICES = (
        ("house", "house"),
        ("user", "user"),
        ("bed", "bed")
    )

    house = models.ForeignKey('HouseInfo', verbose_name='房子', on_delete=models.CASCADE)
    type = models.CharField(max_length=128, verbose_name='房子类型')
    type_name = models.CharField(max_length=10, choices=DISPLAY_TYPE_CHOICES, verbose_name='类型名称')

    class Meta:
        db_table = 'mak_houseType'
        verbose_name = '房子类型'
        verbose_name_plural = verbose_name


class HouseImage(BaseModel):
    house = models.ForeignKey('HouseInfo', verbose_name='房子', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='house', verbose_name='图片路径')

    class Meta:
        db_table = 'mak_house_image'
        verbose_name = '房子图片'
        verbose_name_plural = verbose_name


class House_Facility(BaseModel):
    def __str__(self):
        return (self.house.title + self.facility)

    DISPLAY_TYPE_CHOICES = (
        ("wirelessnetwork", "无线网络"),
        ("shower", "热水淋浴"),
        ("aircondition", "空调"),
        ("heater", "暖气"),
        ("smoke", "允许吸烟"),
        ("drinking", "饮水设备"),
        ("brush", "牙具"),
        ("soap", "香皂"),
        ("slippers", "拖鞋"),
        ("toiletpaper", "手纸"),
        ("towel", "毛巾"),
        ("toiletries", "沐浴露、洗发露"),
        ("icebox", "冰箱"),
        ("washer", "洗衣机"),
        ("elevator", "电梯"),
        ("iscook", "允许做饭"),
        ("pet", "允许带宠物"),
        ("meet", "允许聚会"),
        ("accesssys", "门禁系统"),
        ("parkingspace", "停车位"),
        ("wirednetwork", "有线网络"),
        ("tv", "电视"),
        ("jinzhi", "浴缸"),
    )

    house = models.ForeignKey('HouseInfo', verbose_name='房子', on_delete=models.CASCADE)
    facility = models.CharField(max_length=30, choices=DISPLAY_TYPE_CHOICES, verbose_name='房子设施')


    class Meta:
        db_table = 'mak_house_facility'
        verbose_name = '房子配套设施'
        verbose_name_plural = verbose_name


class IndexHouseBanner(BaseModel):
    '''首页轮播图'''

    def __str__(self):
        return self.house.title

    house = models.ForeignKey('HouseInfo', verbose_name='房子', on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name='轮播标题')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')  # 0 1 2 3

    class Meta:
        db_table = 'mak_IndexHouseBanner'
        verbose_name = '房子轮播图'
        verbose_name_plural = verbose_name
