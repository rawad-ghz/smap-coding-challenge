# -*- coding: utf-8 -*-
"""consumption application URLs"""
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^user/$', views.dashboard, name='users'),
    # url(r'^user/detail/(\d+)/$', views.user_detail, name="user_detail"),
    url(
        r'^user/detail/(?P<pk>[^/]+)/$',
        views.UserDetailView.as_view(),
        name="user_detail",

    ),
    url(r'^area/detail/([\w\-]+)/$', views.area_detail, name="area_detail"),

    url(r'^api/areas/([\w\-]+)/$', views.area_data_by_month, name="api_area"),
    url(
        r'^api/consumption/$',
        views.consumption_view,
        name="api_consumption",
    ),
    url(
        r'^api/consumption/monthly/$',
        views.data_by_month,
        name="api_monthly_consumption",
    ),
    url(
        r'^api/consumption/(\d+)/$',
        views.user_data_by_month,
        name="api_user_consumption",
    ),
]
