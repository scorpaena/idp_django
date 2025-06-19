import json
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from user_account.models import User


class Command(BaseCommand):
    help = 'Generate test data for User model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_companies',
            type=int,
            default=5,
            help='Number of companies to be used in generation (default=5)',
        )
        parser.add_argument(
            '--num_users',
            type=int,
            default=10,
            help='Number of users to generate (default=10)',
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_companies = kwargs['num_companies']
        num_users = kwargs['num_users']
        roles = [choice[0] for choice in User.ROLE_CHOICES]
        companies = list(range(1, num_companies + 1))
        fixture = []

        for pk in range(1, num_users + 1):
            fixture.append(
                {
                    "model": "user_account.user",
                    "pk": pk,
                    "fields": {
                        "username": fake.user_name(),
                        "password": "pbkdf2_sha256$870000$COi1GsJL9JJTeQQwqYE52f$cA3mlQEI7oZvgzBEPpTm9euYkydMcezqq8s55F2pMsc=", # 123
                        "role": random.choice(roles),
                        "company": random.choice(companies)
                    }
                }
            )

        with open(f"{settings.BASE_DIR}/fixtures/user_account.json", "w") as f:
            json.dump(fixture, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Test data generation complete: successfully input `{num_users}` users into fixture file.'))
