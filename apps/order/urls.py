"""anjiaRent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from order.views import BookingView, BookSuccessView, orderListView, orderDetailView


app_name = 'anjiaRent'
urlpatterns = [
    path('book', BookingView.as_view(), name='book'),
    path('success', BookSuccessView.as_view(), name='success'),
    path('olist', orderListView.as_view(), name='olist'),
    path('odetail', orderDetailView.as_view(), name='odetail')

]
