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
from house.views import IndexView, DetailView, searchView, CollectView, survey, surveyhouse
app_name = 'anjiaRent'

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),
    re_path(r'^detail/(?P<house_id>\d+)', DetailView.as_view(), name='detail'),
    path('search', searchView.as_view(), name='search'),
    path('collect', CollectView.as_view(), name='collect'),
    path('survey', survey.as_view(), name='survey'),
    # shehousefloororibed
    re_path(r'^surveylist/she(?P<fac>\d+)house(?P<house>\d+)floor(?P<floor>\d+)ori(?P<ori>\d+)bed(?P<bed>\d+)', surveyhouse.as_view(), name='surveylist')
    # path('insert', insertHouse.as_view(), name='insert')
]
