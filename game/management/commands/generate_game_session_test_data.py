import json
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from game.models import GameSession
import random


class Command(BaseCommand):
    help = 'Generate test data for GameSession model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_game_sessions',
            type=int,
            default=100,
            help='Number of game sessions to generate (default=100)',
        )
        parser.add_argument(
            '--num_games',
            type=int,
            default=10,
            help='Number of games to be used in generation (default=10)',
        )
        parser.add_argument(
            '--num_users',
            type=int,
            default=10,
            help='Number of users to be used in generation (default=10)',
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_game_sessions = kwargs['num_game_sessions']
        num_games = kwargs['num_games']
        num_users = kwargs['num_users']
        statuses = [choice[0] for choice in GameSession._meta.get_field('status').choices]
        games = list(range(1, num_games + 1))
        users = list(range(1, num_users + 1))
        fixture = []

        for pk in range(1, num_game_sessions + 1):
            fixture.append(
                {
                    "model": "game.gamesession",
                    "pk": pk,
                    "fields": {
                        "game": random.choice(games),
                        "user": random.choice(users),
                        "status": random.choice(statuses),
                        "session_date": fake.date(),
                    }
                }
            )

        with open(f"{settings.BASE_DIR}/fixtures/game_session.json", "w") as f:
            json.dump(fixture, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Test data generation complete: successfully input `{num_games}` games sessions into fixture file.'))
