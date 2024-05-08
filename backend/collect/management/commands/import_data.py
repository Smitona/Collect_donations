import csv
from pathlib import Path

import requests
from io import BytesIO

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File

from collect.models import Collect, Payment, User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='The path to the CSV file'
        )

    def handle(self, *args, **options):
        csv_path = options['path'] or str(
            Path(settings.BASE_DIR) / 'data',
        )

        self.import_csv_data(
            csv_path, 'users.csv',
            self.import_users
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Users imported successfully.'
            )
        )

        self.import_csv_data(
            csv_path, 'collects.csv',
            self.import_collects
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Collects imported successfully.'
            )
        )

        self.import_csv_data(
            csv_path, 'payments.csv',
            self.import_payments
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Payments imported successfully.'
            )
        )

    def import_csv_data(self, csv_path, filename, import_func):
        file_path = Path(csv_path) / filename
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            csv_data = csv.DictReader(file, delimiter=',')
            import_func(csv_data)

    def import_users(self, csv_data):
        try:
            if not User.objects.all().exists():
                users = [User(
                    email=row['email'],
                    username=row['username'],
                    password=row['password']
                ) for row in csv_data
                ]
                User.objects.bulk_create(users)
        except ValueError:
            print('Users already imported.')

    def import_collects(self, csv_data):
        try:
            if not Collect.objects.all().exists():
                for row in csv_data:
                    collect = Collect.objects.create(
                        title=row['title'],
                        author=User.objects.get(id=row['author']),
                        goal=row['goal'],
                        goal_amount=row['goal_amount'],
                        description=row['description'],
                        due_to=row['due_to']
                    )

                    filename = row['image'].split('/')[-1]

                    img = requests.get(row['image'], verify=False)
                    buf = BytesIO()
                    buf.write(img.content)

                    collect.image.save(filename, File(buf, img))

        except ValueError:
            print('Collects already imported.')

    def import_payments(self, csv_data):
        try:
            if not Payment.objects.all().exists():
                payments = [Payment(
                    amount=row['amount'],
                    comment=row['comment'],
                    donator=User.objects.get(id=row['donator']),
                    donation_to=Collect.objects.get(id=row['donation_to']),
                    date=row['date'],
                ) for row in csv_data
                ]
                Payment.objects.bulk_create(payments)
        except ValueError:
            print('Payments already imported.')
