# -*- coding: utf-8 -*-
"""views tests"""
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse

from consumption.models import User


class TestViews(TestCase):
    """views tests"""
    @classmethod
    def setUpClass(cls):
        """setup test data"""
        User.objects.create(id=300, area_code='a1', tariff_code='t1'),
        # required
        cls.cls_atomics = cls._enter_atomics()

    def test_home(self):
        client = Client()
        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def area_detail(self):
        client = Client()
        response = client.get(reverse('area_detail', args=['a1']))
        self.assertEqual(response.status_code, 200)

    def user_detail(self):
        client = Client()
        response = client.get(reverse('user_detail', args=[300]))
        self.assertEqual(response.status_code, 200)
