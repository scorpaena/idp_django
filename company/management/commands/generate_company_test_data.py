import json
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker


class Command(BaseCommand):
    help = 'Generate test data for Company model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_companies',
            type=int,
            default=5,
            help='Number of companies to generate (default=5)',
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_companies = kwargs['num_companies']
        fixture = []

        for pk in range(1, num_companies + 1):
            fixture.append(
                {
                    "model": "company.company",
                    "pk": pk,
                    "fields": {
                        "name": f"{pk}_{fake.company()}",
                        "address": fake.address(),
                        "phone_number": fake.phone_number(),
                        "email": fake.email()
                    }
                }
            )

        with open(f"{settings.BASE_DIR}/fixtures/company.json", "w") as f:
            json.dump(fixture, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Test data generation complete: successfully input `{num_companies}` companies into fixture file.'))
