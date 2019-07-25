# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    area_code = models.CharField(max_length=150)
    tariff_code = models.CharField(max_length=150)


class UserConsumption(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    consumption = models.FloatField(default=0.0)
