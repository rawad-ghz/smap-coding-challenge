# -*- coding: utf-8 -*-
"""REST API tests"""
from __future__ import unicode_literals

from django.urls import reverse
import datetime as dt
from collections import OrderedDict
import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from consumption.models import User, UserConsumption
from consumption.serializers import UserSummarySerializer

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def datetime(string, datetime_format=None):
    """returns datetime object from formatted datetime string"""
    return dt.datetime.strptime(string, datetime_format or DATETIME_FORMAT)


class APITest(APITestCase):

    @classmethod
    def setUpClass(cls):
        """setup test data"""
        # could load data from CSVs

        users = [
            User(id=101, area_code='a1', tariff_code='t1'),
            User(id=102, area_code='a1', tariff_code='t2'),
            User(id=103, area_code='a2', tariff_code='t1'),
            User(id=104, area_code='a2', tariff_code='t1'),
            User(id=105, area_code='a2', tariff_code='t1'),
        ]
        consumptions = [
            UserConsumption(user_id=101, consumption=100, start=datetime('2019-01-01 00:00:00'), end=datetime('2019-01-01 00:30:00')),
            UserConsumption(user_id=101, consumption=200, start=datetime('2019-01-01 00:30:00'), end=datetime('2019-01-01 01:00:00')),
            UserConsumption(user_id=102, consumption=300, start=datetime('2019-01-01 00:00:00'), end=datetime('2019-01-01 00:30:00')),
            UserConsumption(user_id=102, consumption=400, start=datetime('2019-01-01 00:30:00'), end=datetime('2019-01-01 01:00:00')),
            UserConsumption(user_id=103, consumption=500, start=datetime('2019-01-01 00:00:00'), end=datetime('2019-01-01 00:30:00')),
            UserConsumption(user_id=103, consumption=600, start=datetime('2019-01-01 00:30:00'), end=datetime('2019-01-01 01:00:00')),
            UserConsumption(user_id=104, consumption=700, start=datetime('2019-01-01 00:00:00'), end=datetime('2019-01-01 00:30:00')),
            UserConsumption(user_id=104, consumption=800, start=datetime('2019-01-01 00:30:00'), end=datetime('2019-01-01 01:00:00')),
            UserConsumption(user_id=105, consumption=900, start=datetime('2019-01-01 00:00:00'), end=datetime('2019-01-01 00:30:00')),
            UserConsumption(user_id=105, consumption=1000, start=datetime('2019-01-01 00:30:00'), end=datetime('2019-01-01 01:00:00')),
        ]
        User.objects.bulk_create(users)
        UserConsumption.objects.bulk_create(consumptions)

        # required
        cls.cls_atomics = cls._enter_atomics()

    def test_users_inserted(self):
        self.assertEqual(User.objects.count(), 5)

    def test_user_consumption_inserted(self):
        self.assertEqual(UserConsumption.objects.count(), 10)

    def test_users_api(self):
        self.maxDiff = None
        client = APIClient()
        response = client.get(reverse('api_consumption'), format='json')
        expected = [
            dict(pk='101', tariff_code='t1', area_code='a1', average=150.0, total=300.0),
            dict(pk='102', tariff_code='t2', area_code='a1', average=350.0, total=700.0),
            dict(pk='103', tariff_code='t1', area_code='a2', average=550.0, total=1100.0),
            dict(pk='104', tariff_code='t1', area_code='a2', average=750.0, total=1500.0),
            dict(pk='105', tariff_code='t1', area_code='a2', average=950.0, total=1900.0),
        ]
        serializer = UserSummarySerializer(expected, many=True)
        self.assertSequenceEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_monthly_api(self):
        self.maxDiff = None
        client = APIClient()
        response = client.get(reverse('api_monthly_consumption'))
        expected = [
            dict(year_month='2019-01', sum=5500.0, count=5)
        ]
        self.assertSequenceEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_api(self):
        self.maxDiff = None
        client = APIClient()
        response = client.get(reverse('api_user_consumption', args=['101']))
        expected = [
            dict(year_month='2019-01', average=150.0, total=300.0)
        ]
        self.assertSequenceEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_area_api(self):
        self.maxDiff = None
        client = APIClient()
        response = client.get(reverse('api_area', args=['a1']))
        expected = [
            dict(year_month='2019-01', average=250.0, total=1000.0, minimum=100, maximum=400)
        ]
        self.assertSequenceEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
