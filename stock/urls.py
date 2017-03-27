from django.conf.urls import url
from . import views
from django.conf.urls import  include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create_company/$', views.create_company, name='create_company'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^company/(?P<company_id>[0-9]+)/$', views.company_detail, name='company_detail'),
    url(r'^company/(?P<company_id>[0-9]+)/visualize/$', views.stock_chart_view, name='stock_chart_view'),
]