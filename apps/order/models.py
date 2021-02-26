from django.db import models
from db.base_model import BaseModel


# Create your models here.

class Comment(BaseModel):
    def __str__(self):
        return self.comment
    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE)
    house = models.ForeignKey('house.HouseInfo', verbose_name='房子', on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, default='', verbose_name='评论')

    class Meta:
        db_table = 'mak_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class order(BaseModel):
    def __str__(self):
        return self.order_id

    order_statue = (
        (0, '已完成'),
        (1, '待支付'),
        (2, '待入住')
    )
    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
    user = models.ForeignKey('user.User', verbose_name='用户', null=True, on_delete=models.SET_NULL)
    house = models.ForeignKey('house.HouseInfo', verbose_name='房子', null=True, on_delete=models.SET_NULL)
    inTime = models.DateTimeField(verbose_name='入住时间')
    outTime = models.DateTimeField(verbose_name='退房时间')
    unitPrice = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='价格')
    allPrice = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='总价')
    comment = models.ForeignKey('Comment', verbose_name='评论', null=True, blank=True, on_delete=models.SET_NULL)
    orderStatue = models.SmallIntegerField(choices=order_statue, verbose_name='订单状态')

    class Meta:
        db_table = 'mak_order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
