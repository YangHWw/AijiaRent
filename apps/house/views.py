from django.urls import reverse
from django.db.models import Q
from datetime import date, datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django_redis import get_redis_connection
from house.models import HouseImage, HouseInfo, Area, HouseType, House_Facility, IndexHouseBanner
from order.models import Comment, order
from user.models import User
from django.core.paginator import Paginator
import json
import random


# Create your views here.

# 127.0.0.1:8000/index
class IndexView(View):
    def get(self, request):
        areas = Area.objects.all()
        houses = HouseInfo.objects.all().order_by('-id')[0:20]
        houseBanner = IndexHouseBanner.objects.all().order_by('index')
        context = {
            'areas': areas,
            'houses': houses,
            'houseBanner': houseBanner,
        }

        return render(request, 'index.html', context)


# /search
class searchView(View):
    '''房子搜索页'''

    def get(self, request):
        areas = Area.objects.all()
        urlinfo = {}
        urlinfo['aid'] = request.GET.get('aid')
        aname = request.GET.get('aname')
        if aname == '':
            aname = '光明区'
        urlinfo['aname'] = aname
        urlinfo['sd'] = request.GET.get('sd')
        urlinfo['ed'] = request.GET.get('ed')
        sort = request.GET.get('sort')
        if sort is None:
            sort = 'new'
        urlinfo['sort'] = sort

        now = datetime.now()
        if urlinfo['sd'] == '' and urlinfo['ed'] == '':
            st = [now.year, now.month, now.day]
            et = [now.year + 1, now.month, now.day]
        elif urlinfo['sd'] != '' and urlinfo['ed'] == '':
            stimeSplit = urlinfo['sd'].split('-')
            st = list(map(int, [stimeSplit[0], stimeSplit[1], stimeSplit[2]]))
            et = [now.year + 1, now.month, now.day]
        else:
            stimeSplit = urlinfo['sd'].split('-')
            etimeSplit = urlinfo['ed'].split('-')
            st = list(map(int, [stimeSplit[0], stimeSplit[1], stimeSplit[2]]))
            et = list(map(int, [etimeSplit[0], etimeSplit[1], etimeSplit[2]]))

        # 获取对应时间段内可以预定的房子
        # 1. 先从订单中获取对应时间段内不能预定的房子
        # 2. 在所有的房子中排除掉不能预定的房子即为可以预定的房子

        # 1.
        statue1 = Q(inTime__gt=date(st[0], st[1], st[2])) & Q(outTime__lt=date(et[0], et[1], et[2]))
        statue2 = Q(inTime__lt=date(st[0], st[1], st[2])) & Q(outTime__gt=date(st[0], st[1], st[2]))
        statue3 = Q(inTime__lt=date(et[0], et[1], et[2])) & Q(outTime__gt=date(et[0], et[1], et[2]))
        # 从订单中获取在对那个时间点有订单的且订单状态为待入住的（即不能预定的）
        isTimeOrder = order.objects.filter(statue1 | statue2 | statue3).exclude(orderStatue__in=[0, 1])
        # 获得不能预定的房子id
        isHouseId = []
        for o in isTimeOrder:
            isHouseId.append(o.house.id)
        # 2.
        house = HouseInfo.objects.exclude(id__in=isHouseId)
        # print(house.filter(area__name='南山区'))
        if urlinfo['sort'] == 'new':
            house = house.filter(area__name=urlinfo['aname'], isBook=False).order_by('id')
        elif urlinfo['sort'] == 'booking':
            house = house.filter(area__name=urlinfo['aname'], isBook=False).order_by('-comment_count')
        elif urlinfo['sort'] == 'inc':
            house = house.filter(area__name=urlinfo['aname'], isBook=False).order_by('price')
        elif urlinfo['sort'] == 'des':
            house = house.filter(area__name=urlinfo['aname'], isBook=False).order_by('-price')

        paginator = Paginator(house, 30)
        try:
            page = int(request.GET.get('page'))
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        house_page = paginator.page(page)

        # todo:进行页码控制，页面上最多显示5个页码
        # 1.总页数小于5页， 页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前两页，当前页，当前页后两页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        context = {
            'areas': areas,
            'urlinfo': urlinfo,
            'house_page': house_page,
            'pages': pages,
        }

        return render(request, 'search.html', context)

    def post(self, request):
        # return redirect(reverse('house:index'))
        return JsonResponse({'res': 1})


# 127.0.0.1:8000/detail/house_id
class DetailView(View):
    '''房子详情'''

    def get(self, request, house_id):
        images = HouseImage.objects.filter(house_id=house_id)
        house = HouseInfo.objects.get(id=house_id)
        types_house = HouseType.objects.filter(house_id=house_id, type_name="house")
        types_user = HouseType.objects.filter(house_id=house_id, type_name="user")
        types_bed = HouseType.objects.filter(house_id=house_id, type_name="bed")
        facilitys = House_Facility.objects.filter(house_id=house_id)
        comments = Comment.objects.filter(house_id=house_id)

        user = request.user
        collect = 0
        if user.is_authenticated:
            conn = get_redis_connection('default')
            collect_key = 'collect_%d' % user.id
            if conn.sismember(collect_key, house.id):
                collect = 1
            else:
                collect = 0
            print('collect', collect)
        context = {
            'images': images,
            'house': house,
            'types_house': types_house,
            'types_user': types_user,
            'types_bed': types_bed,
            'facilitys': facilitys,
            'comments': comments,
            'collect': collect
        }

        return render(request, 'detail.html', context)


# /collect
class CollectView(View):
    # 处理收藏逻辑
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            statue = request.POST.get('statue')
            house_id = request.POST.get('houseid')
            conn = get_redis_connection('default')
            collect_key = 'collect_%d' % user.id
            print(type(statue))
            # 加入收藏
            # redis 集合 (collect_user.id houseid)
            if statue == '1':
                conn.sadd(collect_key, house_id)
                res = 1
                print('加入收藏')
            elif statue == '0':
                # 取消收藏
                conn.srem(collect_key, house_id)
                res = 0
                print('取消收藏')
            return JsonResponse({'res': res})

        else:
            return JsonResponse({'res': 2})


# 127.0.0.1:8000/survey
class survey(View):
    def get(self, request):
        areas = Area.objects.all()
        context = {
            'areas': areas
        }
        return render(request, 'survey.html', context)

    def post(self, request):
        choice = json.loads(request.POST.get('choice'))
        housedict = {'1室1厅': 1, '2室1厅': 2, '3室1厅': 3, '2室2厅': 4, '3室2厅': 5, '5室1厅': 6}
        facility = {'空调': 1, '暖气': 2, '电视': 3, '冰箱': 4, '洗衣机': 5, '电梯': 6, '有线网络': 7, '无线网络': 8}
        oridict = {'东': 1, '南': 2, '西': 3, '北': 4, '东南': 5, '东北': 6, '西南': 7, '西北': 8}
        floor = {'低楼层': 1, '中楼层': 2, '高楼层': 3}
        bed = {'单人床': 1, '双人床': 2, '大床': 3}
        # 获取对应名字的数字代码
        urlfacility = 'she'
        if len(choice[1]) != 0:
            for fl in choice[1]:
                urlfacility += str(facility[fl])
        else:
            urlfacility += '0'

        urlhouse = 'house'
        if len(choice[2]) != 0:
            for hl in choice[2]:
                urlhouse += str(housedict[hl])
        else:
            urlhouse += '0'

        urlfloor = 'floor'
        if len(choice[3]) != 0:
            for floorl in choice[3]:
                urlfloor += str(floor[floorl])
        else:
            urlfloor += '0'

        urlori = 'ori'
        if len(choice[4]) != 0:
            for ol in choice[4]:
                urlori += str(oridict[ol])
        else:
            urlori += '0'

        urlbed = 'bed'
        if len(choice[5]) != 0:
            for bl in choice[5]:
                urlbed += str(bed[bl])
        else:
            urlbed += '0'

        url = urlfacility + urlhouse + urlfloor + urlori + urlbed
        print(url)
        if len(choice[0]) == 0:
            return JsonResponse({
                'res': 0,
                'err': '请选择地区'
            })

        return JsonResponse({
            'res': 1,
            'url1': url,
            'area': choice[0][0]
        })


class surveyhouse(View):

    def getDictKey(self, myDict, value):
        keyList = []
        for k, v in myDict.items():
            if v == value:
                keyList.append(k)
        return keyList

    def get(self, request, fac, house, floor, ori, bed):
        print(fac, house, floor, ori, bed)
        housedict = {'1室1厅': 1,
                     '2室1厅': 2,
                     '3室1厅': 3,
                     '2室2厅': 4,
                     '3室2厅': 5,
                     '5室1厅': 6}

        facility = {'aircondition': 1,
                    'heater': 2,
                    'tv': 3,
                    'icebox': 4,
                    'washer': 5,
                    'elevator': 6,
                    'wirednetwork': 7,
                    'wirelessnetwork': 8}
        oridict = {'东': 1, '南': 2, '西': 3, '北': 4, '东南': 5, '东北': 6, '西南': 7, '西北': 8}
        floordict = {'低楼层': 1, '中楼层': 2, '高楼层': 3}
        beddict = {'单人床': 1, '双人床': 2, '大床': 3}
        facname = []
        if fac != '':
            if fac == '0':
                facname = list(facility.keys())
            else:
                for f in fac:
                    facname.append(self.getDictKey(facility, int(f))[0])

        houseTypename = []
        if house != '':
            if house == '0':
                houseTypename.append('室')
            else:
                houseTypename = self.getDictKey(housedict, int(house))

        floorname = []
        if floor != '':
            if floor == '0':
                floorname.append('楼层')
            else:
                for fl in floor:
                    floorname.append(self.getDictKey(floordict, int(fl))[0])

        oriname = []
        if ori != '':
            if ori == '0':
                oriname.append('东')
            else:
                for o in ori:
                    oriname.append(self.getDictKey(oridict, int(o))[0])

        bedname = []
        if bed != '':
            if bed == '0':
                bedname = list(beddict.keys())
            else:
                for b in bed:
                    bedname.append(self.getDictKey(beddict, int(b))[0])

        area = request.GET.get('area')
        print(floorname, bedname, houseTypename, oriname, facname, area)
        house = HouseInfo.objects.filter(housetype__type__contains=floorname[0]).filter(housetype__type__in=bedname).filter(
            title__contains=houseTypename[0]).filter(title__contains=oriname[0]).filter(house_facility__facility__in=facname).filter(
            area__name=area).filter(isBook=False)
        print(house)
        if len(house) == 0:
            areas = Area.objects.all()
            return render(request, 'survey.html', {
                'err': '没有适合您的房子,请重试',
                'areas': areas
            })
        context = {
            'house_page':house
        }

        return render(request, 'surveyhouse.html', context)

# class insertHouse(View):
#     def get(self, request):
#
#         with open('F://python/test1/data1.json', 'r') as f:
#             data = json.loads(f.read())
#         # for 遍历数据
#         user = User.objects.get(id=1)
#         # totalh = 0
#         # for i in range(0, 100):
#         #     house_list = []
#         #     eachPage = data[str(i)]
#         #     # print(eachPage)
#         #     page = 'page' + str(i + 1)
#         #     for j in range(1, len(eachPage[page].keys()) + 1):
#         #         # print(eachPage[page][str(j)])
#         #         title = eachPage[page][str(j)]['title']
#         #         addr = eachPage[page][str(j)]['add']
#         #         area = Area.objects.get(name=eachPage[page][str(j)]['add'].split('-')[0])
#         #         price = random.randint(1000, 30000)
#         #         mins = 1
#         #         maxs = 2
#         #         comment_count = 0
#         #         image = eachPage[page][str(j)]['imgUrl']
#         #         house = HouseInfo(user=user,
#         #                           title=title,
#         #                           price=price,
#         #                           addr=addr,
#         #                           area=area,
#         #                           min_stay_day=mins,
#         #                           max_stay_day=maxs,
#         #                           image=image,
#         #                           comment_count=comment_count)
#         #
#         #         house_list.append(house)
#         #     HouseInfo.objects.bulk_create(house_list)  # #批量往数据库中创建数据
#         #     totalh += len(house_list)
#         #     print('house_list', len(house_list))
#         # print('totalh', totalh)
#         totali = 0
#         cf = []
#         fchoice = [("wirelessnetwork", "无线网络"),
#                   ("shower", "热水淋浴"),
#                   ("aircondition", "空调"),
#                   ("heater", "暖气"),
#                   ("smoke", "允许吸烟"),
#                   ("drinking", "饮水设备"),
#                   ("brush", "牙具"),
#                   ("soap", "香皂"),
#                   ("slippers", "拖鞋"),
#                   ("toiletpaper", "手纸"),
#                   ("towel", "毛巾"),
#                   ("toiletries", "沐浴露、洗发露"),
#                   ("icebox", "冰箱"),
#                   ("washer", "洗衣机"),
#                   ("elevator", "电梯"),
#                   ("iscook", "允许做饭"),
#                   ("pet", "允许带宠物"),
#                   ("meet", "允许聚会"),
#                   ("accesssys", "门禁系统"),
#                   ("parkingspace", "停车位"),
#                   ("wirednetwork", "有线网络"),
#                   ("tv", "电视"),
#                   ("jinzhi", "浴缸")]
#         for i in range(0, 100):
#             himg_list = []
#             eachPage = data[str(i)]
#             # print(eachPage)
#             page = 'page' + str(i + 1)
#
#             for j in range(1, len(eachPage[page].keys()) + 1):
#                 ischoice = []
#                 title = eachPage[page][str(j)]['title']
#                 if title in cf:
#                     continue
#                 house = HouseInfo.objects.filter(title=title)
#                 if len(house) != 1:
#                     cf.append(title)
#                     for h in house:
#                         # type = eachPage[page][str(j)]['floor']
#
#                         for ci in range(0, random.randint(7,23)):
#                             facility = random.choice(fchoice)[0]
#                             if facility in ischoice:
#                                 ci -= 1
#                                 continue
#                             ischoice.append(facility)
#
#                             htype = House_Facility(house=h, facility=facility)
#                             himg_list.append(htype)
#                         ischoice=[]
#                 else:
#                     # type = eachPage[page][str(j)]['type']
#                     for ci in range(0, random.randint(7, 23)):
#                         facility = random.choice(fchoice)[0]
#                         if facility in ischoice:
#                             ci -= 1
#                             continue
#                         ischoice.append(facility)
#                         htype = House_Facility(house=house[0], facility=facility)
#                         himg_list.append(htype)
#                     ischoice = []
#
#             House_Facility.objects.bulk_create(himg_list)  # #批量往数据库中创建数据
#             print(len(himg_list))
#             totali += len(himg_list)
#         print('totali', totali)
#         return render(request, 'index.html')
