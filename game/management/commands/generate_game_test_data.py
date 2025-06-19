import json
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker


class Command(BaseCommand):
    help = 'Generate test data for Game model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_games',
            type=int,
            default=10,
            help='Number of games to generate (default=10)',
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_games = kwargs['num_games']
        fixture = []

        for pk in range(1, num_games + 1):
            fixture.append(
                {
                    "model": "game.game",
                    "pk": pk,
                    "fields": {
                        "title": fake.catch_phrase(),
                        "language": fake.language_name(),
                        "category": fake.word(),
                        "release_date": fake.date(),
                    }
                }
            )

        with open(f"{settings.BASE_DIR}/fixtures/game.json", "w") as f:
            json.dump(fixture, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Test data generation complete: successfully input `{num_games}` games into fixture file.'))
