# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Avg, Sum, Min, Max


class User(models.Model):
    area_code = models.CharField(max_length=150)
    tariff_code = models.CharField(max_length=150)

    def user_consumption(self):
        """returns total user consumption summary"""
        return User.objects.filter(
            id=self.id
        ).values(
            'pk', 'area_code', 'tariff_code'
        ).annotate(
            average=Avg('userconsumption__consumption'),
            total=Sum('userconsumption__consumption'),
            minimum=Min('userconsumption__consumption'),
            maximum=Max('userconsumption__consumption'),
        )[0]


class UserConsumption(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    consumption = models.FloatField(default=0.0)
