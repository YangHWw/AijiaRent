from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from house.models import HouseInfo
from order.models import order, Comment
from utils.mixin import LoginRequiredMixin
from datetime import datetime, date
from django.db.models import Q
from random import randint
import re


# Create your views here.

# /order/book
class BookingView(LoginRequiredMixin, View):
    '''预定订单处理'''

    def get(self, request):
        try:
            houseId = request.GET.get('houseId')
            house = HouseInfo.objects.get(id=houseId)
            context = {
                'house': house,
            }

        except HouseInfo.DoesNotExist as e:
            context = {

            }
        return render(request, 'booking.html', context)

    def post(self, request):
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        price = request.POST.get('price')
        amount = request.POST.get('amount')
        beforeurl = request.POST.get('beforeurl')
        house_id = re.match(r'houseId=(\d+)', beforeurl).group(1)
        if not all([startDate, endDate, price, amount]):
            return JsonResponse({'res': 0})
        print('数据', startDate, endDate, price, amount, beforeurl, house_id)

        house = HouseInfo.objects.get(id=house_id)
        sd = startDate.split('-')
        ed = endDate.split('-')
        # 判断该时间段是否有人预定
        st = list(map(int, [sd[0], sd[1], sd[2]]))
        et = list(map(int, [ed[0], ed[1], ed[2]]))
        # 1.先获取该房子与该时间段冲突的订单
        statue1 = Q(inTime__gte=date(st[0], st[1], st[2])) & Q(outTime__lte=date(et[0], et[1], et[2]))
        statue2 = Q(inTime__lte=date(st[0], st[1], st[2])) & Q(outTime__gte=date(st[0], st[1], st[2]))
        statue3 = Q(inTime__lte=date(et[0], et[1], et[2])) & Q(outTime__gte=date(et[0], et[1], et[2]))
        isTimeOrder = order.objects.filter(house=house).filter(statue1 | statue2 | statue3).exclude(
            orderStatue__in=[0, 1])

        if len(isTimeOrder) == 0:

            # 订单号编码：当前日期年月日+（startDate年后两位+月+日）+（endDate年后两位+月+日）+ house_id + user_id
            now = datetime.now()
            user = request.user
            ranStr = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
            print(ranStr)
            order_id = 'O' + str(now.year) + str(now.month) + str(now.day) + ranStr + str(now.hour) + str(
                now.minute) + str(now.second) + str(house_id) + str(user.id)
            order.objects.create(order_id=order_id,
                                 user=user,
                                 house=house,
                                 inTime=startDate,
                                 outTime=endDate,
                                 unitPrice=price,
                                 allPrice=amount,
                                 orderStatue=2)

            return JsonResponse({'res': 1})

        else:
            # 推荐相同地区该时间内的房子
            area = house.area.name
            aid = house.area.id
            return JsonResponse({'res': 0,
                                 'areaname': area,
                                 'aid': aid,
                                 'st': startDate,
                                 'et': endDate})


# /order/success
class BookSuccessView(View):
    '''预定成功跳转函数'''

    def get(self, request):
        return render(request, 'submitorders.html')


# /order/olist
class orderListView(LoginRequiredMixin, View):
    '''订单列表'''

    def get(self, request):
        user = request.user
        orders = user.order_set.all()

        context = {
            'orders': orders
        }

        return render(request, 'lorders.html', context)


# /order/odetail
class orderDetailView(LoginRequiredMixin, View):
    '''订单详情'''

    def get(self, request):
        order_id = request.GET.get('orderid')
        o = order.objects.get(order_id=order_id)
        context = {
            'order': o
        }

        return render(request, 'orderDetail.html', context)

    def post(self, request):
        order_id = request.POST.get('orderid')
        comment = request.POST.get('res')
        if comment != '':
            # 找到对应的订单
            o = order.objects.get(order_id=order_id)
            # 通过订单找到房子
            house = o.house
            house.comment_count += 1
            house.save()
            user = request.user
            c = Comment()
            c.user = user
            c.house = house
            c.comment = comment
            c.save()
            o.comment = c
            o.save()
            return JsonResponse({'res': 1})
        else:
            return JsonResponse({'res': 0})
