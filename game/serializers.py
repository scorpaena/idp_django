from rest_framework import serializers
from game.models import Game, GameSession, GameResult
from user_account.serializers import UserSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'language', 'category', 'release_date']
        read_only_fields = ['id']


class GameSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(
        source='game',
        queryset=Game.objects.all(),
        write_only=True
    )

    class Meta:
        model = GameSession
        fields = ['id', 'game', 'user', 'status', 'session_date', 'game_id']
        read_only_fields = ['id', 'session_date']


class GameResultSerializer(serializers.ModelSerializer):
    session = GameSessionSerializer(read_only=True)
    session_id = serializers.PrimaryKeyRelatedField(
        source='session',
        queryset=GameSession.objects.all(),
        write_only=True
    )

    class Meta:
        model = GameResult
        fields = ['id', 'session', 'score', 'is_completed', 'result_date', 'session_id']
        read_only_fields = ['id', 'result_date', 'session']
