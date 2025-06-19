import json
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Generate test data for GameResult model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_game_results',
            type=int,
            default=100,
            help='Number of game results to generate (default=100)',
        )
        parser.add_argument(
            '--num_game_sessions',
            type=int,
            default=100,
            help='Number of game sessions to be used in generation (default=100)',
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_game_results = kwargs['num_game_results']
        num_game_sessions = kwargs['num_game_sessions']
        game_sessions = list(range(1, num_game_sessions + 1))
        fixture = []

        for pk in range(1, num_game_results + 1):
            fixture.append(
                {
                    "model": "game.gameresult",
                    "pk": pk,
                    "fields": {
                        "session": random.choice(game_sessions),
                        "score": fake.random_int(min=0, max=1000),
                        "is_completed": fake.boolean(),
                        "result_date": fake.date(),
                    }
                }
            )

        with open(f"{settings.BASE_DIR}/fixtures/game_result.json", "w") as f:
            json.dump(fixture, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Test data generation complete: successfully input `{num_game_results}` games results into fixture file.'))
