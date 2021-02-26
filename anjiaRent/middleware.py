from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class HouseDetailReturnMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        print('middle',request.get_full_path())
        print(request)