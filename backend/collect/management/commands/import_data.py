import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from Collect_donations.backend.collect.models import Collect, Payment


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
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_data = csv.DictReader(file)
            import_func(csv_data)

    def import_collects(self, csv_data):
        collects = [Collect(
            title=row['title'],
            author=row['author'],
            image=row['image'],
            goal=row['goal'],
            goal_amount=row['goal_amount'],
            description=row['description'],
            due_to=row['due_to']
        ) for row in csv_data
        ]
        Collect.objects.bulk_create(collects, )

    def import_payments(self, csv_data):
        payments = [Payment(
            amount=row['amount'],
            comment=row['comment'],
            donator=row['donator'],
            donation_to=row['donation_to'],
            date=row['date'],
        ) for row in csv_data
        ]
        Payment.objects.bulk_create(payments)
