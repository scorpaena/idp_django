from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.id} - {self.title}"


class GameSession(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey('user_account.User', on_delete=models.CASCADE, related_name='game_sessions')
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('created', 'Created'),
        ('in_progress', 'In_Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned')
    ], default='active')
    session_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user.username} - {self.game.title} ({self.session_date})"


class GameResult(models.Model):
    session = models.ForeignKey('GameSession', on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    result_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.user.username} - {self.session.game.title} Result ({self.result_date})"
