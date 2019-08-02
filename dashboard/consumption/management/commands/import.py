from datetime import datetime, timedelta
from os.path import exists, basename
import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from consumption.models import User, UserConsumption

DELIMITER = ','
DATA_PATH = '{}/consumption/{}.csv'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CONSUMPTION_INTERVAL = 30  # minutes


class Command(BaseCommand):
    help = 'import users and user consumption data'

    def add_arguments(self, parser):
        """adds needed command arguments"""
        parser.add_argument(
            '-d',
            '--delimiter',
            default=DELIMITER,
            type=str,
            help='delimiting character',
        )
        parser.add_argument(
            '-i',
            '--interval',
            default=CONSUMPTION_INTERVAL,
            type=int,
            help='interval',
        )
        parser.add_argument(
            '-f',
            '--format',
            default=DATETIME_FORMAT,
            type=str,
            help='datetime format',
        )
        parser.add_argument(
            '-s',
            '--silent',
            default=False,
            action='store_true',
            help='do not display messages',
        )
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        """command logic: loads data into database"""

        self.file_path = file_path = options['filepath']
        self.delimiter = options['delimiter']
        self.interval = options['interval']
        self.format = options['format']
        self.silent = options['silent']

        if not exists(file_path):
            raise Exception('file "{}" not found'.format(file_path))
        # get consumption directory path
        self.base_path = file_path[:-(len(basename(file_path)))]
        self.add_users()

    def add_users(self):
        """add users and their respective consumption data from CSV files"""

        with open(self.file_path, 'r') as users_file:
            reader = csv.reader(users_file, delimiter=self.delimiter)
            # skip the header row
            count = 0
            next(reader)
            with transaction.atomic():
                for row in reader:
                    pk, area, tariff = row
                    user_id = int(pk)
                    # create the user if not exists
                    _, created = User.objects.get_or_create(
                        id=user_id,
                        defaults=dict(area_code=area, tariff_code=tariff),
                    )
                    # increment user count for created users
                    if created:
                        count += 1
                    # add user consumption data if file exists
                    user_file_path = DATA_PATH.format(self.base_path, pk)
                    if not exists(user_file_path):
                        continue
                    self.add_user_consumption(user_id, user_file_path)
        if not self.silent:
            self.stdout.write(
                f'Added {count} users and thier respective consumption data')

    def add_user_consumption(self, user_id, user_file_path):
        """bulk insert user consumption data from CSV file"""

        with open(user_file_path, 'r') as consumption_file:
            sub_reader = csv.reader(consumption_file, delimiter=self.delimiter)
            # skip the header row
            next(sub_reader)
            instances = []
            for row2 in sub_reader:
                end = datetime.strptime(row2[0], DATETIME_FORMAT)
                start = end - timedelta(minutes=self.interval)
                consumption = float(row2[1])
                instances.append(
                    UserConsumption(
                        user_id=user_id,
                        start=start,
                        end=end,
                        consumption=consumption,
                    ))
            UserConsumption.objects.bulk_create(instances)
