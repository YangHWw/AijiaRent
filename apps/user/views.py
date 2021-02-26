from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django_redis import get_redis_connection
from PIL import Image, ImageDraw, ImageFont
from utils.mixin import LoginRequiredMixin
from django.views.generic import View
from django.utils.six import BytesIO
from django.urls import reverse
from house.models import HouseInfo
from user.models import User
import re

# Create your views here.

# 生成验证码
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# /user/register
class RegisterView(View):
    '''注册'''
    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        phone = request.POST.get('mobile')
        username = request.POST.get('username')
        vcode = request.POST.get('imagecode')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        vcode2 = request.session.get('verifycode')
        if not all([phone, username, vcode, password, password2]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'register.html', {'errmsg': '手机号码格式不正确'})
        if password != password2:
            return render(request, 'register.html', {'errmsg': '第二次密码不正确'})
        if vcode != vcode2:
            return render(request, 'register.html', {'errmsg': '验证码错误'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名在数据库中不存在
            user = None

        if user:
            # 用户名在数据库中已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        user = User.objects.create_user(username, password=password, phone=phone)
        user.save()
        return redirect(reverse('user:login'))


# /user/login
class LoginView(View):
    '''登录'''
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        user = authenticate(username=username, password=password)

        if user is not None:
            # 记住用户的登陆状态, django内置函数login，会自动将用户保存在session中
            login(request, user)
            # 获取登陆后索要跳转的地址
            # 默认跳转到首页
            print(request.META)
            next_url = request.GET.get('next', reverse('house:index'))
            print(next_url)
            response = redirect(next_url)
            return response
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


class LogoutView(View):
    '''退出登录'''

    def get(self, request):
        '''退出登录'''
        # 清除用户session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('house:index'))


# /user/my
class myInfoView(View):
    def get(self, request):
        return render(request, 'my.html')


# /user/collect
class myhouseView(LoginRequiredMixin, View):
    def get(self, request):
        conn = get_redis_connection('default')
        user = request.user
        collect_key = 'collect_%d' % user.id
        houseIds = list(conn.smembers(collect_key))
        houseIds = list(map(int, houseIds))
        houses = HouseInfo.objects.filter(id__in=houseIds)
        context = {
            'houses':houses,
        }

        return render(request, 'myhouse.html', context)