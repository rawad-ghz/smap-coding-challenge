# -*- coding: utf-8 -*-
"""database queries"""
from __future__ import unicode_literals

from django.db import models
from django.db.models import Avg, Sum, Func, Min, Max, Count

from consumption.models import User, UserConsumption


class YearMonth(Func):
    """UserConsumption start column filter to filter by month of year %Y-%m"""
    template = "substr(start, 0, 8)"
    output_field = models.CharField()


def user_summary():
    """returns summary grouped by user_id"""
    return User.objects.values(
        'pk', 'area_code', 'tariff_code'
    ).annotate(
        average=Avg('userconsumption__consumption'),
        total=Sum('userconsumption__consumption'),
    )


def user_monthly_summary(user_id):
    """returns summary grouped by user_id and month"""
    return (
        UserConsumption.objects
        .filter(user_id=user_id)
        .annotate(year_month=YearMonth())
        .values('year_month')
        .annotate(
            average=Avg('consumption'),
            total=Sum('consumption'),
        )
        .order_by()
    )


def area_monthly_summary(area_code):
    """returns summary grouped by area code"""
    return (
        UserConsumption.objects.filter(user__area_code=area_code)
        .annotate(year_month=YearMonth())
        .values('year_month')
        .annotate(
            average=Avg('consumption'),
            total=Sum('consumption'),
            minimum=Min('consumption'),
            maximum=Max('consumption'),
        )
        .order_by()
    )


def area_summary(area_code):
    """returns area summary"""
    return (
        UserConsumption.objects.filter(user__area_code=area_code)
        .values('user__area_code')
        .annotate(
            average=Avg('consumption'),
            total=Sum('consumption'),
        )
        .order_by()
    )[0]


def monthly_summary():
    """returns consumption sum grouped by user_count and month of year"""
    return (
        UserConsumption.objects
        .annotate(year_month=YearMonth()).values('year_month')
        .annotate(
            count=Count('user_id', distinct=True),
            sum=Sum('consumption'))
    )
