# -*- coding: utf-8 -*-
"""Management commands tests"""
from __future__ import unicode_literals
from os.path import dirname, join

from django.test import TestCase
from django.core import management

from consumption.models import User, UserConsumption


FILE_PATH = __file__
CSV_FILE_NAME = 'user_data.csv'
DATA_DIRECTORY_NAME = 'data'


class ImportDataTest(TestCase):
    """Import Data management command test class"""

    def test_users_inserted(self):
        """
        tests import data
        using sample user_data CSV file and user consumption CSV files
        """
        csv_file_path = join(
            dirname(FILE_PATH), DATA_DIRECTORY_NAME, CSV_FILE_NAME)

        management.call_command('import', csv_file_path, silent=True)

        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(UserConsumption.objects.count(), 50)
